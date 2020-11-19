package com.jamesfchen.river.wrappers;

import android.os.IBinder;
import android.os.IInterface;

import java.lang.reflect.Method;

/**
 * Copyright ® $ 2020
 * All right reserved.
 *
 * @author: jf.chen
 * @email: jf.chen@Ctrip.com
 * @since: Nov/19/2020  Thu
 */
public final class ServiceManager {
    private WallpaperManager wallpaperManager;
    private final Method getServiceMethod;

    public ServiceManager() {
        try {
            getServiceMethod = Class.forName("android.os.ServiceManager").getDeclaredMethod("getService", String.class);
        } catch (Exception e) {
            throw new AssertionError(e);
        }
    }

    private IInterface getService(final String service,final String type) {
        try {
            IBinder binder = (IBinder) getServiceMethod.invoke(null, service);
            Method asInterfaceMethod = Class.forName(type + "$Stub").getMethod("asInterface", IBinder.class);
            return (IInterface) asInterfaceMethod.invoke(null, binder);
        } catch (Exception e) {
            throw new AssertionError(e);
        }
    }

    public WallpaperManager getWallpaperManager() {
        if (wallpaperManager == null) {
            wallpaperManager = new WallpaperManager(getService("wallpaper", "android.app.IWallpaperManager"));
        }
        return wallpaperManager;
    }
}
