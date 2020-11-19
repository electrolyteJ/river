#!/bin/bash
./gradlew assembleDebug
adb push /Users/jf.chen/crawler/river/android/app/build/outputs/apk/debug/app-debug.apk /data/local/tmp/server-debug.apk
./run.sh