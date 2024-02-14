# Program to have client & server having heartbeat

## Logic
1. Strart Client & Server
2. Server sending "heartbeat" to client
3. If client doesn't receives it for 3 consecutive attempts it re-initiates connection with server

## /etc/hosts setting
- 127.0.0.1 notifier  (attempt-1)
- 172.16.0.1 notifier  (replaced in attempt-2)
## Client-Side Code
```
import asyncio

async def heartbeat_client(host, port):
    try:
        while True:
            reader, writer = await asyncio.open_connection(host, port)
            print("Connected to server.")

            readAttemptFailed = 0

            while readAttemptFailed < 3:
                try:
                    data = await asyncio.wait_for(reader.read(1024), 5)
                    if data:
                        print("Received heartbeat from server:", data.decode())
                        readAttemptFailed = 0
                except asyncio.TimeoutError:
                    print("Timeout occurred while waiting for data.")
                    writer.close()
                    try:
                        await writer.wait_closed()
                    except BrokenPipeError:
                        print("Broken pipe - Connection already closed.")
                    break
                except Exception as e:
                    print(e)

                readAttemptFailed = readAttemptFailed + 1
                await asyncio.sleep(5)

    except asyncio.CancelledError:
        pass
    finally:
        print(f"All is well: Finally")

async def tcp_reconnect(host, port):
    server = '{} {}'.format(host, port)
    while True:
        print('Connecting to server {} ...'.format(server))
        try:
            await heartbeat_client(host, port)
        except ConnectionRefusedError:
            print('Connection to server {} failed!'.format(server))
        except asyncio.TimeoutError:
            print('Connection to server {} timed out!'.format(server))
        else:
            print('Connection to server {} is closed.'.format(server))
        await asyncio.sleep(2.0)


if __name__ == "__main__":
    host = "notifier"
    port = 8888
    asyncio.run(tcp_reconnect(host, port))
```

## Server-Side Code
```
import asyncio

async def handle_client(reader, writer):
    print("Client connected.")
    try:
        while True:
            writer.write(b"Heartbeat\n")
            await writer.drain()
            await asyncio.sleep(4)  # Send heartbeat every 5 seconds
    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        pass
    finally:
        print("Client disconnected.")
        writer.close()
        try:
            await writer.wait_closed()
        except BrokenPipeError:
            print("Broken pipe - Connection already closed.")

async def heartbeat_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    async with server:
        print(f"Server running on {host}:{port}")
        await server.serve_forever()

if __name__ == "__main__":
    host = ""
    port = 8888
    asyncio.run(heartbeat_server(host, port))
```
