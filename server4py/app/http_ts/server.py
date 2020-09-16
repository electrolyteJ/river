import uvloop
import asyncio
from aiohttp import web


# //localhost:8081/live/movie0.m3u8
# //localhost: 8081/live/xxxx.ts


async def handle_root(request):
    # print(request.url.path)
    return web.json_response("handle_root")


async def handle_m3u8(request):
    with open('1967.mp3.m3u8', 'r') as f:
        b = f.read().encode("utf-8")

    headers = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "audio/x-mpegurl",
        "Content-Disposition": "inline; filename=\"{}\"".format("1967.mp3.m3u8"),
        'Content-Length': 111
    }
    print('cjf-handle_m3u8', '\n', headers, '\n', b.decode('utf-8'))
    return web.Response(body=b, headers=headers)


async def handle_ts(request):
    ts_path = request.match_info["ts_path"]
    print('cjf-handle_ts', '\n', ts_path)
    resp = web.StreamResponse(
        reason='OK',
        headers={
            "Content-Type": "video/mp2ts",
            'Content-Length': 111
        })
    await resp.prepare(request)
    for _ in range(1000000):
        await resp.write(b'Hello world')
        await resp.drain()  # switch point
    await resp.write_eof()
    return resp


def cors_headers():
    headers = {
        "Access-Control-Allow-Origin": "*"
    }
    return headers


async def handle_preflight(request):
    return web.Response()


async def cors_middleware(app, handler):
    async def middleware_handler(request):
        if request.method == "OPTIONS":
            response = await handle_preflight(request)
        else:
            response = await handler(request)
        response.headers.update(cors_headers())
        return response

    return middleware_handler


def main():
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # loop = asyncio.get_event_loop()
    # app = web.Application(middlewares=[cors_middleware])
    app = web.Application()
    app.add_routes([web.get('/', handle_root),
                    web.get('/live/movie0.m3u8', handle_m3u8),
                    web.get('/live/movie/{ts_path}', handle_ts),
                    ])
    web.run_app(app, port=8081)


if __name__ == '__main__':
    main()
