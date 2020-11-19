package com.jamesfchen.river.wrappers;

import android.app.IWallpaperManagerCallback;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.Rect;
import android.os.Bundle;
import android.os.IInterface;
import android.os.ParcelFileDescriptor;
import android.os.RemoteException;
import android.util.Log;

import java.io.FileOutputStream;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;

/**
 * Copyright ® $ 2020
 * All right reserved.
 *
 * @author: jf.chen
 * @email: jf.chen@Ctrip.com
 * @since: Nov/19/2020  Thu
 */
public final class WallpaperManager {
//    public static final String PACKAGE_NAME = "com.hawksjamesf.spacecraft.debug";
//    public static final String PACKAGE_NAME = "com.jamesfchen.river";
//    public static final int USER_ID = 1000;
//    public static final String PACKAGE_NAME = "com.android.systemui";
//    public static final int USER_ID = 1000;
    public static final String PACKAGE_NAME = "com.android.shell";
    public static final int USER_ID = 0;
    private final IInterface manager;
    private Method setWallpaperMethod;
    public static final int FLAG_LOCK = 1 << 1;
    public static final int FLAG_SYSTEM = 1 << 0;
    public static final String EXTRA_NEW_WALLPAPER_ID = "android.service.wallpaper.extra.ID";

    public WallpaperManager(IInterface manager) {
        this.manager = manager;
    }

    private final void validateRect(Rect rect) {
        if (rect != null && rect.isEmpty()) {
            throw new IllegalArgumentException("visibleCrop rectangle must be valid and non-empty");
        }
    }

    public void setBitmap(Bitmap bitmap) throws IOException {
        setBitmap(bitmap, null, true);
    }

    public int setBitmap(Bitmap fullImage, Rect visibleCropHint, boolean allowBackup) throws IOException {
        return setBitmap(fullImage, visibleCropHint, allowBackup, FLAG_SYSTEM | FLAG_LOCK);
    }

    public int setBitmap(Bitmap fullImage, Rect visibleCropHint, boolean allowBackup, int which) throws IOException {
        return setBitmap(fullImage, visibleCropHint, allowBackup, which, USER_ID);
//                mContext.getUserId());
    }

    public int setBitmap(Bitmap fullImage, Rect visibleCropHint, boolean allowBackup, int which, int userId)
            throws IOException {
        validateRect(visibleCropHint);
        if (manager == null) {
            Log.w("cjf", "WallpaperService not running");
            throw new RuntimeException();
        }
        final Bundle result = new Bundle();
        final WallpaperSetCompletion completion = new WallpaperSetCompletion();
        try {
            ParcelFileDescriptor fd = setWallpaper(null, PACKAGE_NAME, visibleCropHint, allowBackup, result, which, completion, userId);
            if (fd != null) {
                FileOutputStream fos = null;
                try {
                    fos = new ParcelFileDescriptor.AutoCloseOutputStream(fd);
                    fullImage.compress(Bitmap.CompressFormat.PNG, 90, fos);
                    fos.close();
                    completion.waitForCompletion();
                } finally {
                    if (fos != null) {
                        fos.close();
                    }
                }
            }
        } catch (RemoteException e) {
//            throw e.rethrowFromSystemServer();
        }
        return result.getInt(EXTRA_NEW_WALLPAPER_ID, 0);
    }

    public ParcelFileDescriptor setWallpaper(String name, String callingPackage, Rect cropHint, boolean allowBackup, Bundle extras, int which, WallpaperSetCompletion completion, int userid) throws RemoteException {
        try {
            Method[] methods = manager.getClass().getMethods();
            for (Method m : methods) {

                Log.d("cjf", "method:"+m.getName());
            }
            if (setWallpaperMethod == null) {
                setWallpaperMethod = manager.getClass().getMethod("setWallpaper", String.class, String.class, Rect.class, boolean.class, Bundle.class, int.class, IWallpaperManagerCallback.class, int.class);
            }
            return (ParcelFileDescriptor) setWallpaperMethod.invoke(manager, name, callingPackage, cropHint, allowBackup, extras, which, completion, userid);
        } catch (InvocationTargetException | IllegalAccessException | NoSuchMethodException e) {
            Log.e("cjf", "Could not invoke method", e);
            e.printStackTrace();
            return null;
        }
    }
    public static String getUid(Context context) {
        String uid = "";
        try {
            PackageManager pm = context.getPackageManager();//com.android.shell
            ApplicationInfo ai = pm.getApplicationInfo("com.android.systemui", PackageManager.GET_META_DATA);
            uid = String.valueOf(ai.uid);
        } catch (PackageManager.NameNotFoundException e) {
            e.printStackTrace();
        }
        return uid;
    }

    private class WallpaperSetCompletion extends IWallpaperManagerCallback.Stub {
        final CountDownLatch latch;

        public WallpaperSetCompletion() {
            this.latch = new CountDownLatch(1);
        }

        public void waitForCompletion() {
            try {
                latch.await(30, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onWallpaperChanged() {
            latch.countDown();
        }

    }
}
