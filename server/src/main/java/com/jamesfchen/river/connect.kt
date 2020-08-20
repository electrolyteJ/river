package com.jamesfchen.river

import android.net.LocalSocket
import android.net.LocalSocketAddress
import java.io.Closeable
import java.io.IOException

/**
 * Copyright ® $ 2017
 * All right reserved.
 *
 * @author: hawks.jamesf
 * @since: Aug/15/2020  Sat
 */
private const val SOCKET_NAME = "river"

@Throws(IOException::class)
private fun connect(abstractName: String): LocalSocket {
    val localSocket = LocalSocket()
    localSocket.connect(LocalSocketAddress(abstractName))
    return localSocket
}


@Throws(IOException::class)
fun open(device: Device, tunnelForward: Boolean): DesktopConnection {
    val connection = DesktopConnection()
    val connect = connect(SOCKET_NAME)
//    val videoSize: Size = device.getScreenInfo().getVideoSize()
//    connection.send(Device.getDeviceName(), videoSize.getWidth(), videoSize.getHeight())
    return connection
}

class Device {

}

class DesktopConnection : Closeable {
    private val socketMap = HashMap<String, LocalSocket>()
    fun putSocket(name: String, socket: LocalSocket) {
        socketMap[name] = socket
    }

    override fun close() {
        for ((n, s) in socketMap) {
            s.shutdownInput()
            s.shutdownOutput()
            s.close()
        }
    }

}