import http.server
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import os
import socket


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class RHandler(SimpleHTTPRequestHandler):

    pass


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    # print('local ip', get_host_ip())
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
    run(handler_class=RHandler)


if __name__ == '__main__':
    main()
