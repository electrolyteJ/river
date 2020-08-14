    adb shell CLASSPATH=/data/local/tmp/classes.dex \
        app_process / my.package.MainClass

adb reverse
```bash
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

# adb reverse tcp:PORT   localabstract:jfc
