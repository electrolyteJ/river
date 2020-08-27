from aiohttp import web


def main():
    async def handle(request):
        name = request.match_info.get('name', "Anonymous")
        return web.Response(text=('hello, ' + name))
    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])
    web.run_app(app)


if __name__ == '__main__':
    main()
