@file:JvmName("WallpaperServer")
package com.jamesfchen.river

import android.app.WallpaperManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.util.Log
import com.blankj.utilcode.util.ConvertUtils
import com.blankj.utilcode.util.ImageUtils
import com.jamesfchen.river.wrappers.ServiceManager
import java.io.File

fun main(args: Array<String>) {
    val serviceManager = ServiceManager()
    val file = File("/sdcard/cjf.jpg")
//    val stringExtra = intent?.getStringExtra("imei") ?: "NA"
    val wallpaperManager = serviceManager.wallpaperManager
    val myBitmap: Bitmap = BitmapFactory.decodeFile(file.absolutePath)
    Log.d("cjf", "file:" + file.absoluteFile)
//    val addTextWatermark = ImageUtils.addTextWatermark(myBitmap, "stringExtra", ConvertUtils.dp2px(70f), Color.BLUE, 10f, 20f)
    wallpaperManager.setBitmap(myBitmap)

}