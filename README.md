river is live project which include push stream side , process stream side , pull stream side。

### Mobile Side
- [x] Desktop

- [ ] Video window

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





