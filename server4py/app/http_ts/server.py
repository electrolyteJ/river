# import uvloop
import asyncio
from aiohttp import web
from app.container import ts
from app.codec import h264
from app.http_ts import m3u8
import queue
import threading
from app.container import ts
from app.codec import h264
from app.http_ts import server
import time
import asyncio


# //localhost:8081/live/movie0.m3u8
# //localhost: 8081/live/xxxx.ts

async def handle_root(request):
    # print(request.url.path)
    return web.json_response("handle_root")


q = queue.Queue()
muxer = ts.Muxer(strategy=ts.Strategy.WRITE_TO_MEMORY)


def consumer():
    while True:
        f = q.get()
        ts_packet_list = muxer.muxe(f)
        muxer.write(ts_packet_list.payload)
        q.task_done()


MIN_SIZE = 2

M3U8_DURATION = 7

buffer = {}


async def handle_m3u8(request):
    print('>>>', 'handle_m3u8 start')
    segs = []
    l = muxer.cache.get(3)
    for ts_file in l:
        buffer[ts_file.name] = ts_file
        segs.append(m3u8.Segment(ts_file.duration/1000 if ts_file.duration/1000 <= M3U8_DURATION else M3U8_DURATION, '',
                                 '/live/movie/%s' % ts_file.name))
    m = m3u8.M3u8(M3U8_DURATION, segs)
    m3u8_file: str = m3u8.gen_live(m)
    # with open('movie0.m3u8', 'r') as f:
    #     m3u8_file = f.read()
    print('>>>', 'handle_m3u8\n', m3u8_file)
    m3u8_bytes = m3u8_file.encode('utf-8')
    resp = web.StreamResponse(
        reason='OK',
        headers={
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache",
            "Content-Type": "audio/x-mpegurl",
            # "Content-Disposition": "inline; filename=\"{}\"".format("movie.m3u8"),
            'Content-Length': str(len(m3u8_bytes))
        })

    await resp.prepare(request)
    await resp.write(m3u8_bytes)
    # await resp.drain()  # switch point
    await resp.write_eof()
    print('>>>', 'handle_m3u8 end')
    return resp


async def handle_ts(request):
    print('>>>', 'handle_ts start')
    ts_path = request.match_info["ts_path"]
    print('>>>', 'handle_ts', ts_path)
    ts_block = buffer.pop(ts_path)
    if ts_block is None:
        print('>>>', 'handle_ts ts_block is empty', )
        return web.Response()
    resp = web.StreamResponse(
        reason='OK',
        headers={
            "Content-Type": "video/mp2ts",
            'Content-Length': str(len(ts_block.b))
        })
    await resp.prepare(request)
    await resp.write(ts_block.b)
    # await resp.drain()  # switch point
    await resp.write_eof()
    print('>>>', 'handle_ts end')
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


port = 9000


def start_server():
    threading.Thread(target=consumer).start()

    app = web.Application()
    app.add_routes([web.get('/', handle_root),
                    web.get('/live/movie.m3u8', handle_m3u8),
                    web.get('/live/movie/{ts_path}', handle_ts),
                    ])
    # web.run_app(app, port=9000)
    runner = web.AppRunner(app)
    return runner


# kill tcp process :sudo lsof -i tcp:9000
def main():
    hls_server_loop = asyncio.new_event_loop()
    print('start_hls_server >>>> ', hls_server_loop.time(), end='\n')
    print('http://0.0.0.0:%d/live/movie.m3u8' % port)
    asyncio.set_event_loop(hls_server_loop)
    runner = start_server()
    hls_server_loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', port)
    hls_server_loop.run_until_complete(site.start())
    hls_server_loop.run_forever()


if __name__ == '__main__':
    main()
