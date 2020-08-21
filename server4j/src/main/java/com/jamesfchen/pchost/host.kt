@file:JvmName("Host")
package com.jamesfchen.pchost

import java.io.BufferedReader
import java.io.File
import java.io.InputStream
import java.io.InputStreamReader
import java.net.InetSocketAddress
import java.net.ServerSocket
import java.util.concurrent.Executors
import java.util.function.Consumer
import kotlin.concurrent.thread


const val TAG = "jfc-host"
private const val SOCKET_NAME = "jfc"
fun main(args: Array<String>) {
    thread {
        val server = ServerSocket()
        val serverAdd = InetSocketAddress(27184)
        server.bind(serverAdd)
        val client = server.accept()
        println("client add : ${client.inetAddress}")
        while (true) {
            println("client state ${client.isClosed} ${client
                    .isConnected}")
            val readLine = client.getInputStream().bufferedReader().readLine()
            if (readLine.isNullOrEmpty()) continue
//            println("read:$readLine")
        }
    }
    val isWindows = System.getProperty("os.name")
            .toLowerCase().startsWith("windows")
    val builder = ProcessBuilder()
    if (isWindows) {
        builder.command("cmd.exe", "/c", "dir")
    } else {
        builder.command("sh", "-c", "adb reverse  localabstract:river tcp:27184")
    }
    builder.directory(File(System.getProperty("user.home")))
    val process = builder.start()
    val streamGobbler = StreamGobbler(process.inputStream, Consumer<String> {
        println("$it")
    })
    Executors.newSingleThreadExecutor().submit(streamGobbler)
    val exitCode = process.waitFor()
    assert(exitCode == 0)
}
class StreamGobbler(private val inputStream: InputStream, private val consumer: Consumer<String>) : Runnable {

    override fun run() {
        BufferedReader(InputStreamReader(inputStream)).lines()
            .forEach(consumer)
    }
}



