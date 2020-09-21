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
from aiohttp import web

if __name__ == '__main__':
    print('=' * 60, end='\n')
    print('\n')
    print('>>> start local socket server slide', end='\n')
    print('\n')
    threading.Thread(target=localsocket_server.main).start()
    print('>>> start http-ts server slide', end='\n')
    print('\n', end='\n')
    threading.Thread(target=http_ts_server.main).start()
    print('=' * 60, end='\n')
