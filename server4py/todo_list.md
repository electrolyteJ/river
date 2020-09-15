 
## ts，test_ts.py
 - ~~整个pat + pmt+ pes包有大小限制~~
 - ~~ts 提供readable接口，供外部调用~~
 
 
 ## 整个项目的架构
 - 拉流端，推流端
 - container、protocol 、 codec 等基础设施
 - uuid:一个拉流用户对应一个设备推流，暂时不去实现一个设备推流多个拉流用户