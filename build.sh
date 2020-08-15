#!/bin/bash
./gradlew assembleDebug
adb push /Users/hawks.jamesf/tech/crawler/river/server/build/outputs/apk/debug/server-debug.apk /data/local/tmp/server-debug.apk
./run.sh