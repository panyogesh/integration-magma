#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>
#include <sys/queue.h>
#include <errno.h>
#include <signal.h>

#include <rte_memory.h>
#include <rte_launch.h>
#include <rte_eal.h>
#include <rte_per_lcore.h>
#include <rte_lcore.h>
#include <rte_debug.h>
#include <rte_mempool.h>
#include <rte_ring.h>
#include <rte_mbuf.h>

#define BURST_SIZE 32

static struct rte_mempool *mbuf_pool;
static struct rte_ring *send_ring, *recv_ring;
static volatile int force_quit = 0;

static void signal_handler(int signum)
{
    if (signum == SIGINT || signum == SIGTERM) {
        printf("\nSignal %d received, preparing to exit...\n", signum);
        force_quit = 1;
    }
}

static int secondary_loop(__rte_unused void *dummy)
{
    struct rte_mbuf *bufs[BURST_SIZE];
    struct rte_mbuf *tx_bufs[BURST_SIZE];
    unsigned nb_rx, nb_tx;
    int i;
    char *data;
    static uint32_t counter = 0;

    printf("Secondary process started on lcore %u\n", rte_lcore_id());

    while (!force_quit) {
        /* Receive messages from primary process */
        nb_rx = rte_ring_dequeue_burst(send_ring, (void **)bufs, BURST_SIZE, NULL);
        if (nb_rx > 0) {
            printf("Received %u messages from primary:\n", nb_rx);
            for (i = 0; i < nb_rx; i++) {
                data = rte_pktmbuf_mtod(bufs[i], char *);
                printf("  [%d]: %s\n", i, data);
                rte_pktmbuf_free(bufs[i]);
            }

            /* Send response messages back to primary */
            nb_tx = rte_mempool_get_bulk(mbuf_pool, (void **)tx_bufs, nb_rx);
            if (nb_tx == 0) {
                for (i = 0; i < nb_rx; i++) {
                    data = rte_pktmbuf_mtod(tx_bufs[i], char *);
                    snprintf(data, 64, "Secondary response %u", counter++);
                    tx_bufs[i]->data_len = strlen(data) + 1;
                    tx_bufs[i]->pkt_len = tx_bufs[i]->data_len;
                }

                nb_tx = rte_ring_enqueue_burst(recv_ring, (void **)tx_bufs, nb_rx, NULL);
                if (nb_tx < nb_rx) {
                    /* Free unsent mbufs */
                    for (i = nb_tx; i < nb_rx; i++) {
                        rte_pktmbuf_free(tx_bufs[i]);
                    }
                }
                printf("Sent %u response messages to primary\n", nb_tx);
            }
        }

        rte_delay_ms(100); /* 100ms delay */
    }

    return 0;
}

int main(int argc, char *argv[])
{
    int ret;
    unsigned lcore_id;

    /* Initialize EAL as secondary process */
    ret = rte_eal_init(argc, argv);
    if (ret < 0)
        rte_panic("Cannot init EAL\n");

    /* Install signal handlers */
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    /* Lookup mempool created by primary */
    mbuf_pool = rte_mempool_lookup("MBUF_POOL");
    if (mbuf_pool == NULL)
        rte_exit(EXIT_FAILURE, "Cannot find mbuf pool\n");

    /* Lookup rings created by primary */
    send_ring = rte_ring_lookup("PRIMARY_TO_SECONDARY");
    if (send_ring == NULL)
        rte_exit(EXIT_FAILURE, "Cannot find PRIMARY_TO_SECONDARY ring\n");

    recv_ring = rte_ring_lookup("SECONDARY_TO_PRIMARY");
    if (recv_ring == NULL)
        rte_exit(EXIT_FAILURE, "Cannot find SECONDARY_TO_PRIMARY ring\n");

    printf("Secondary process initialized successfully\n");
    printf("Found - Mempool: %s, Send Ring: %s, Recv Ring: %s\n",
           mbuf_pool->name, send_ring->name, recv_ring->name);

    /* Launch secondary loop on main lcore */
    lcore_id = rte_get_next_lcore(-1, 1, 0);
    if (lcore_id == RTE_MAX_LCORE) {
        /* Run on main lcore if no worker lcore available */
        secondary_loop(NULL);
    } else {
        rte_eal_remote_launch(secondary_loop, NULL, lcore_id);
        rte_eal_wait_lcore(lcore_id);
    }

    /* Cleanup */
    rte_eal_cleanup();

    return 0;
}
