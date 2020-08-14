#!/bin/bash
adb shell CLASSPATH=/data/local/tmp/server-debug.apk exec app_process /system/bin com.jamesfchen.river.Server "$@"
