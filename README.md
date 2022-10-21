River is live stream project which include push stream side , process stream side , pull stream side。

### Mobile Side
- [x] Desktop

- [ ] Camera

### Web Back End Side

#### Push Stream Server
- [x] h264 codec + local socket protocol

- [ ] h264 codec + flv container + rtmp protocol

#### Pull Stream Server
- [x] h264 codec + ts container + http-ts protocol

- [ ] h264 codec + flv container + http-flv protocol

- [ ] h264 codec + flv container + rtmp protocol

### Web Front End Side
- [x] http-ts/HLS:`http://0.0.0.0:9000/live/movie.m3u8` 

- [ ] http-flv:`http://0.0.0.0:9000/live/movie.flv`

- [ ] rtmp:`http://0.0.0.0:9000/live/movie`

## Get Start

|Android(push stream side)|Server(process stream side)|WebApp / VLC App(pull stream side)
|---|---|---|
[install SpacecraftAndroid app](https://github.com/Spacecraft-Plan/SpacecraftAndroid/)|start server: `python main.py`|listening url: `http://0.0.0.0:9000/live/movie.m3u8` 

## Contribution


```bash
Local表示电脑，Remote表示手机，adb forward 电脑 手机，表示将电脑端口数据转发到手机端口，adb reverse 手机 电脑，表示将手机端口数据转发到电脑端口

localabstract 使用android的LocalSocket或者LocalServerSocket

tcp 使用WebSocket或者Socket

networking:
 connect HOST[:PORT]      connect to a device via TCP/IP [default port=5555]
 disconnect [HOST[:PORT]]
     disconnect from given TCP/IP device [default port=5555], or all
 forward --list           list all forward socket connections
 forward [--no-rebind] LOCAL REMOTE
     forward socket connection using:
       tcp:<port> (<local> may be "tcp:0" to pick any open port)
       localabstract:<unix domain socket name>
       localreserved:<unix domain socket name>
       localfilesystem:<unix domain socket name>
       dev:<character device name>
       jdwp:<process pid> (remote only)
 forward --remove LOCAL   remove specific forward socket connection
 forward --remove-all     remove all forward socket connections
 ppp TTY [PARAMETER...]   run PPP over USB
 reverse --list           list all reverse socket connections from device
 reverse [--no-rebind] REMOTE LOCAL
     reverse socket connection using:
       tcp:<port> (<remote> may be "tcp:0" to pick any open port)
       localabstract:<unix domain socket name>
       localreserved:<unix domain socket name>
       localfilesystem:<unix domain socket name>
 reverse --remove REMOTE  remove specific reverse socket connection
 reverse --remove-all     remove all reverse socket connections from device
```

## debug server
```
adb forward tcp:5005 tcp:5005

In Android Studio, _Run_ > _Debug_ > _Edit configurations..._ On the left, click on
`+`, _Remote_, and fill the form:

 - Host: `localhost`
 - Port: `5005`

```

[hls](https://tools.ietf.org/html/rfc8216)
## stream server
aiohttp sqlalchemy asyncio






