import asyncio
import subprocess
import os
from app.byte_ext import read64be, read32be
from asyncio.streams import StreamReader, StreamWriter
from app.container import ts
from app.codec import h264
from app.http_ts import server as http_ts_server
from app.android_localsocket import server as localsocket_server
import time
import asyncio
import threading

if __name__ == '__main__':
    print('=' * 60)
    print('\n')
    print('>>> start local socket server slide')
    print('\n')
    # threading.Thread(target=localsocket_server.main).start()
    subprocess.run('python3 /Users/hawks.jamesf/tech/crawler/river/server4py/app/android_localsocket/server.py',
                   shell=True)
    print('>>> start http-ts server slide')
    print('\n')
    # threading.Thread(target=http_ts_server.main).start()
    subprocess.run('python3 /Users/hawks.jamesf/tech/crawler/river/server4py/app/http_ts/server.py', shell=True)
    print('=' * 60)
