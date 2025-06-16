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

#define RING_SIZE 1024
#define MEMPOOL_SIZE 8192
#define MBUF_CACHE_SIZE 256
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

static int primary_loop(__rte_unused void *dummy)
{
    struct rte_mbuf *bufs[BURST_SIZE];
    struct rte_mbuf *tx_bufs[BURST_SIZE];
    unsigned nb_rx, nb_tx;
    int i;
    char *data;
    static uint32_t counter = 0;

    printf("Primary process started on lcore %u\n", rte_lcore_id());

    while (!force_quit) {
        /* Send messages to secondary process */
        nb_tx = rte_mempool_get_bulk(mbuf_pool, (void **)tx_bufs, BURST_SIZE);
        if (nb_tx == 0) {
            for (i = 0; i < BURST_SIZE; i++) {
                data = rte_pktmbuf_mtod(tx_bufs[i], char *);
                snprintf(data, 64, "Primary message %u", counter++);
                tx_bufs[i]->data_len = strlen(data) + 1;
                tx_bufs[i]->pkt_len = tx_bufs[i]->data_len;
            }

            nb_tx = rte_ring_enqueue_burst(send_ring, (void **)tx_bufs, BURST_SIZE, NULL);
            if (nb_tx < BURST_SIZE) {
                /* Free unsent mbufs */
                for (i = nb_tx; i < BURST_SIZE; i++) {
                    rte_pktmbuf_free(tx_bufs[i]);
                }
            }
            printf("Sent %u messages to secondary\n", nb_tx);
        }

        /* Receive messages from secondary process */
        nb_rx = rte_ring_dequeue_burst(recv_ring, (void **)bufs, BURST_SIZE, NULL);
        if (nb_rx > 0) {
            printf("Received %u messages from secondary:\n", nb_rx);
            for (i = 0; i < nb_rx; i++) {
                data = rte_pktmbuf_mtod(bufs[i], char *);
                printf("  [%d]: %s\n", i, data);
                rte_pktmbuf_free(bufs[i]);
            }
        }

        rte_delay_ms(1000); /* 1 second delay */
    }

    return 0;
}

int main(int argc, char *argv[])
{
    int ret;
    unsigned lcore_id;

    /* Initialize EAL */
    ret = rte_eal_init(argc, argv);
    if (ret < 0)
        rte_panic("Cannot init EAL\n");

    /* Install signal handlers */
    signal(SIGINT, signal_handler);
    signal(SIGTERM, signal_handler);

    /* Create mempool for mbufs */
    mbuf_pool = rte_pktmbuf_pool_create("MBUF_POOL", MEMPOOL_SIZE,
        MBUF_CACHE_SIZE, 0, RTE_MBUF_DEFAULT_BUF_SIZE, rte_socket_id());
    if (mbuf_pool == NULL)
        rte_exit(EXIT_FAILURE, "Cannot create mbuf pool\n");

    /* Create rings for IPC */
    send_ring = rte_ring_create("PRIMARY_TO_SECONDARY", RING_SIZE,
        rte_socket_id(), RING_F_SP_ENQ | RING_F_SC_DEQ);
    if (send_ring == NULL)
        rte_exit(EXIT_FAILURE, "Cannot create send ring\n");

    recv_ring = rte_ring_create("SECONDARY_TO_PRIMARY", RING_SIZE,
        rte_socket_id(), RING_F_SP_ENQ | RING_F_SC_DEQ);
    if (recv_ring == NULL)
        rte_exit(EXIT_FAILURE, "Cannot create recv ring\n");

    printf("Primary process initialized successfully\n");
    printf("Mempool: %s, Send Ring: %s, Recv Ring: %s\n",
           mbuf_pool->name, send_ring->name, recv_ring->name);

    /* Launch primary loop on main lcore */
    lcore_id = rte_get_next_lcore(-1, 1, 0);
    if (lcore_id == RTE_MAX_LCORE) {
        /* Run on main lcore if no worker lcore available */
        primary_loop(NULL);
    } else {
        rte_eal_remote_launch(primary_loop, NULL, lcore_id);
        rte_eal_wait_lcore(lcore_id);
    }

    /* Cleanup */
    rte_mempool_free(mbuf_pool);
    rte_ring_free(send_ring);
    rte_ring_free(recv_ring);
    rte_eal_cleanup();

    return 0;
}
