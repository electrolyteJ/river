import asyncio
import websockets


async def hello(websocket, path):
    async for message in websocket:
        print('server received :', message)
        await websocket.send(message)
        if message is None:
            continue
        print(f"< {message}")

        greeting = f"Hello {message}!"

        await websocket.send(greeting)
        print(f"> {greeting}")

start_server = websockets.serve(hello, '10.32.151.21', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
