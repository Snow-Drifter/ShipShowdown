import asyncio
from typing import Callable

HOST = '127.0.0.1'
PORT = 8888


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter, _queue):
    print("Client connected")
    request = None
    try:
        maintain_connection = True
        while maintain_connection:
            # wait until a request is received. store it in a 255 byte buffer
            input = await reader.read(255)
            
            # input is empty if the client got disconnected
            if input == b'':
                break

            print("Request received")

            # decode request
            request = input.decode()
            if request == 'leave':
                # handle client leaving server
                writer.write("goodbye".encode())
                maintain_connection = False
            elif "retarded" in request:
                # kick client for saying retarded (for the lulz)
                writer.write("kicked".encode())
                maintain_connection = False
            else:
                # confirm that their message has been received
                writer.write("message:message received".encode())

            await writer.drain()

        print("Client disconnected")
    except KeyboardInterrupt:
        print("Thread closed due to KeyboardInterrupt")
    finally:
        writer.close()


def handle_client_with_queue(queue) -> Callable[[asyncio.StreamReader, asyncio.StreamWriter, asyncio.Queue], None]:
    return lambda read, write: handle_client(read, write, queue)


async def server():
    print("Server started")
    queue = asyncio.Queue()
    # call handle_client whenever a connection is made
    server = await asyncio.start_server(handle_client_with_queue(queue), HOST, PORT)
    async with server:
        await server.serve_forever()

try:
    asyncio.run(server())
except KeyboardInterrupt:
    print("Shutting down...")
