import asyncio
from gdio.Client import Client

async def connect():
    return await asyncio.open_connection('localhost', 19734)

async def main():
    reader, writer = await connect()

    client = Client(None, None, None)

    requestInfo = await client.InitHandshake(writer)
    print(f'Recieved: {await client.Receive(reader)}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())