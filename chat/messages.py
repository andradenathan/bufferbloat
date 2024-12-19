import socket
import threading
import time
import random
from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.quic.configuration import QuicConfiguration
import asyncio

MESSAGE_SIZE = 128 
MESSAGE_INTERVALS = (0.05, 0.5) 
NUM_MESSAGES = 100 
PROTOCOLS = ["TCP", "QUIC"] 

def server(port, protocol):
    if protocol == "TCP":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("127.0.0.1", port))
        server_socket.listen(1)
        print(f"TCP server listening on port {port}")
        conn, _ = server_socket.accept()
        
        for _ in range(NUM_MESSAGES):
            data = conn.recv(MESSAGE_SIZE)
            if not data:
                break
            print(f"TCP server received message: {data[:10]}...")
        conn.close()
        server_socket.close()

    elif protocol == "QUIC":
        asyncio.run(quic_server(port))

async def quic_server(port):
    class ServerProtocol(QuicConnectionProtocol):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.messages_received = 0

        def quic_event_received(self, event):
            from aioquic.quic.events import StreamDataReceived
            if isinstance(event, StreamDataReceived):
                self.messages_received += 1
                print(f"QUIC server received message {self.messages_received}: {event.data[:10]}...")
                if self.messages_received >= NUM_MESSAGES:
                    print("QUIC server received all messages.")

    configuration = QuicConfiguration(is_client=False)
    print(f"QUIC server starting on port {port}")
    server = await asyncio.start_server(
        lambda: ServerProtocol(configuration=configuration), "127.0.0.1", port
    )
    async with server:
        await server.serve_forever()

def client(port, protocol):
    if protocol == "TCP":
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("127.0.0.1", port))
        print(f"TCP client connected to port {port}")

        for i in range(NUM_MESSAGES):
            message = b"x" * MESSAGE_SIZE
            client_socket.send(message)
            print(f"TCP client sent message {i + 1}")
            time.sleep(random.uniform(*MESSAGE_INTERVALS))
        client_socket.close()

    elif protocol == "QUIC":
        asyncio.run(quic_client(port))

async def quic_client(port):
    configuration = QuicConfiguration(is_client=True)
    print(f"QUIC client connecting to port {port}")
    async with connect("127.0.0.1", port, configuration=configuration) as connection:
        for i in range(NUM_MESSAGES):
            message = b"x" * MESSAGE_SIZE
            await connection.send_stream_data(0, message, end_stream=False)
            print(f"QUIC client sent message {i + 1}")
            await asyncio.sleep(random.uniform(*MESSAGE_INTERVALS))

def simulate_protocol(protocol):
    port = random.randint(5000, 6000) 

    server_thread = threading.Thread(target=server, args=(port, protocol))
    server_thread.start()

    time.sleep(1)

    start_time = time.time()
    client(port, protocol)
    end_time = time.time()

    server_thread.join()

    total_time = end_time - start_time
    print(f"Protocol: {protocol} | Total Time: {total_time:.2f} seconds")

for protocol in PROTOCOLS:
    simulate_protocol(protocol)