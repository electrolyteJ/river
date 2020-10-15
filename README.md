> hi river
river 是一个从移动端推流，web后端处理流，web前端拉流的项目。

### 移动端流源头

-[x] 桌面

-[ ] 视频

### web后端流处理

#### 推流端服务
-[x] h264 codec + local socket protocol

-[ ] h264 codec + flv container + rtmp protocol

#### 拉流端服务
-[x] h264 codec + ts container + http-ts protocol

-[ ] h264 codec + flv container + http-flv protocol

-[ ] h264 codec + flv container + rtmp protocol

### web前端流拉取
-[x] http-ts/HLS:`http://0.0.0.0:9000/live/movie.m3u8` 

-[ ] http-flv:http://0.0.0.0:9000/live/movie.flv

-[ ] rtmp:http://0.0.0.0:9000/live/movie

## Get Start

|Android(push stream side)|Server(process stream side)|WebApp / VLC App(pull stream side)
|---|---|---|
[install SpacecraftAndroid app](https://github.com/Spacecraft-Plan/SpacecraftAndroid/)|start server: `python main.py`|listening url: `http://0.0.0.0:9000/live/movie.m3u8` 





