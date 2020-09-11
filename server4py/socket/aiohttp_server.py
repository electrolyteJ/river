# import pyrebase
# config = {
#     'apiKey': 'AIzaSyCgJOEsq12RhD9EOBBnR1VSZNSvCW1Sdtg',
#     'authDomain': 'spacecraft-22dc1.firebaseapp.com',
#     'databaseURL': 'https://spacecraft-22dc1.firebaseio.com',
#     'projectId': 'spacecraft-22dc1',
#     'storageBucket': 'spacecraft-22dc1.appspot.com',
#     'messagingSenderId': '28459008283',
#     'appId': "1:28459008283:web:809f4571433c65f9",
#     'measurementId': "G-83LV95LTW7"
#     }
# firebase = pyrebase.initialize_app(config)
# storage = firebase.storage()
# u = storage.child("/audio/1967.mp3").get_url('https://firebasestorage.googleapis.com/v0/b/spacecraft-22dc1.appspot.com/o/audio%2F1967.mp3?alt=media&token=ba945066-4714-4340-82a3-d26d4a22cb3b')
# print(u)
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
