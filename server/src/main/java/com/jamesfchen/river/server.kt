@file:JvmName("Server")
package com.jamesfchen.river

import android.net.LocalSocket
import android.net.LocalSocketAddress
import android.util.Log
import com.blankj.utilcode.util.NetworkUtils
import com.jamesfchen.river.C.ClientConnect
import okio.internal.commonToUtf8String
import java.io.BufferedReader
import java.io.IOException
import java.io.InputStreamReader

const val TAG="jfc-server"
fun main(args: Array<String>) {
//    if (args.size == 0) {
//        C.printHelp()
//        return
//    }
//    var command = ""
//    for (i in args.indices) {
//        command = command + args[i] + " "
//        Log.w(TAG, "command$command")
//    }
//    val cl = ClientConnect()
//    cl.connect()
//    cl.send(command)
//    val result = cl.recv()
//    println("java client recive:$result")
//    cl.close()
//    val localServerSocket =LocalServerSocket(SOCKET_NAME)
//    try {
//        videoSocket = localServerSocket.accept()
//        // send one byte so the client may read() to detect a connection error
//        videoSocket.outputStream.write(0)
//        try {
//           var  controlSocket = localServerSocket.accept()
//        } catch (e: IOException) {
//            videoSocket.close()
//            throw e
//        } catch (e: RuntimeException) {
//            videoSocket.close()
//            throw e
//        }
//    } finally {
//        localServerSocket.close()
//    }
    Log.d(TAG, "main:"+ NetworkUtils.getIPAddress(true))
    val connect = connect(SOCKET_NAME)
    val inputStream = connect?.inputStream
    while (true) {
        var result: String? = null
        try {
            val br = BufferedReader(InputStreamReader(inputStream))
            result = br.readLine()
        } catch (e: IOException) {
            e.printStackTrace()
        } finally {
            if (result.isNullOrEmpty()) continue
            Log.d(TAG, "read:${result}")
        }

    }
}
private const val SOCKET_NAME = "river"
lateinit var videoSocket: LocalSocket
@Throws(IOException::class)
fun connect(abstractName: String): LocalSocket? {
    val localSocket = LocalSocket()
    localSocket.connect(LocalSocketAddress(abstractName))
    return localSocket
}
