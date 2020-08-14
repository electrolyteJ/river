@file:JvmName("Server")
package com.jamesfchen.river

import android.util.Log
import okhttp3.*
import okio.ByteString
import java.util.concurrent.TimeUnit


/**
 * Copyright ® $ 2020
 * All right reserved.
 *
 * @author: jf.chen
 * @email: jf.chen@Ctrip.com
 * @since: Aug/14/2020  Fri
 */

const val TAG="jfc-server"
fun main(args: Array<String>) {
    val eagerClient = OkHttpClient.Builder()
        .readTimeout(500, TimeUnit.MILLISECONDS)
        .build()
    val request = Request.Builder().url("ws://echo.websocket.org").build()
//    val request = Request.Builder().url("ws://10.32.151.21:8765").build()
    val newWebSocket = eagerClient.newWebSocket(request, object : WebSocketListener() {
        override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
            super.onClosed(webSocket, code, reason)
            Log.d(TAG, "onClosed")
        }

        override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
            super.onClosing(webSocket, code, reason)
            Log.d(TAG, "onClosing")
        }

        override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
            super.onFailure(webSocket, t, response)
            Log.d(TAG, "onFailure")
        }

        override fun onMessage(webSocket: WebSocket, text: String) {
            super.onMessage(webSocket, text)
            Log.d(TAG, "onMessage")
        }

        override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
            super.onMessage(webSocket, bytes)
            Log.d(TAG, "onMessage")
        }

        override fun onOpen(webSocket: WebSocket, response: Response) {
            super.onOpen(webSocket, response)
            Log.d(TAG, "onOpen")
        }
    })
    newWebSocket.send("hahah")
    eagerClient.dispatcher.executorService.shutdown();
}