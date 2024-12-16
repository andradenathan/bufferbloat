import asyncio
from aioquic.asyncio import serve
from aioquic.quic.configuration import QuicConfiguration

async def handle_request(stream_reader, stream_writer):
    data = await stream_reader.read(1024)
    print(f"Recebido: {data.decode()}")
    stream_writer.write(b"Resposta do Servidor QUIC")
    await stream_writer.drain()
    stream_writer.close()

def start_server():
    config = QuicConfiguration(is_client=False)
    config.load_cert_chain(certfile="server.crt", keyfile="server.key")
    server = serve("localhost", 4433, configuration=config, stream_handler=handle_request)
    print("Servidor QUIC rodando em localhost:4433")
    return server

if __name__ == "__main__":
    asyncio.run(start_server())
