@file:JvmName("Server")

package com.jamesfchen.river

import android.os.IBinder
import android.util.Log
import com.blankj.utilcode.util.NetworkUtils

const val TAG = "jfc-server"
fun main(args: Array<String>) {
    Log.d(TAG, "main:" + NetworkUtils.getIPAddress(true))
//    val inputStream = connect?.inputStream
//    val br = BufferedReader(InputStreamReader(inputStream))
//    val bufferedWriter = connect?.outputStream?.bufferedWriter()
//    val pw = connect?.outputStream?.let { PrintWriter(it) }
//    while (true) {
//        var result: String? = null
//        try {
////            result = br.readLine()
////            bufferedWriter?.write("haha".toCharArray())
////            bufferedWriter?.flush()
//            pw?.println("haha")
//            pw?.flush()
//        } catch (e: IOException) {
//            e.printStackTrace()
//        } finally {
//            if (result.isNullOrEmpty()) continue
//            Log.d(TAG, "read:${result}")
//        }
//
//    }
    val createDisplay = createDisplay()
    Log.d("cjf", "d:$createDisplay")
}

fun createDisplay(): IBinder? {
    return SurfaceControl.createDisplay("jf", true)
}