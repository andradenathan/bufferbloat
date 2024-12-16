import asyncio
from aioquic.asyncio.protocol import connect
from aioquic.quic.configuration import QuicConfiguration

async def quic_client():
    config = QuicConfiguration(is_client=True)
    async with connect("localhost", 4433, configuration=config) as connection:
        reader, writer = await connection.create_stream()
        writer.write(b"Olá, servidor QUIC!")
        await writer.drain()
        data = await reader.read(1024)
        print(f"Recebido do servidor: {data.decode()}")

if __name__ == "__main__":
    asyncio.run(quic_client())