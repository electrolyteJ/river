package com.jamesfchen.river;

import android.net.LocalSocket;
import android.net.LocalSocketAddress;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;


public class C{
    private static final String TAG = "Factory_test";
    public static void printHelp() {
        System.out.println(
                "\n" +
                        "Usage: factory_test cmds [params]\n" +
                        "cmds:\n" +
                        "        get_eth_mac -- get ethernet mac address.\n" +
                        "        copy_log -- copy the log to usb device .\n"
        );
    }


    public static class ClientConnect {
        private static final String TAG = "ClientConnect";
        private static final String name = "com.penghui.localsocket";
        private LocalSocket Client = null;
        private PrintWriter os = null;
        private BufferedReader is = null;
        private int timeout = 30000;

        public void connect() {
            try {
                Client = new LocalSocket();
                Client.connect(new LocalSocketAddress(name));
                // Client.setSoTimeout(timeout);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public void send(String data) {
            try {
                os = new PrintWriter(Client.getOutputStream());
                os.println(data);
                os.flush();
                //System.out.println("client send over");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        public String recv() {
            Log.d(TAG, "recv");
            String result = null;
            try {
                is = new BufferedReader(new InputStreamReader(Client.getInputStream()));
                result = is.readLine();
                Log.d(TAG, result);
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
            }
            return result;
        }

        public void close() {
            try {
                is.close();
                os.close();
                Client.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
