public class AioSocketClient  implements Runnable{
    private static Integer PORT = 8888;
    private static String IP_ADDRESS = "127.0.0.1";
    private AsynchronousSocketChannel asynSocketChannel ;
    public AioSocketClient() throws Exception {
        asynSocketChannel = AsynchronousSocketChannel.open();  // Open the channel
    }
    public void connect(){
        asynSocketChannel.connect(new InetSocketAddress(IP_ADDRESS, PORT));  // Creating connections is the same as NIO
    }
    public void write(String request){
        try {
            asynSocketChannel.write(ByteBuffer.wrap(request.getBytes())).get();
            ByteBuffer byteBuffer = ByteBuffer.allocate(1024);
            asynSocketChannel.read(byteBuffer).get();
            byteBuffer.flip();
            byte[] respByte = new byte[byteBuffer.remaining()];
            byteBuffer.get(respByte); // Put buffer data into byte arrays
            System.out.println(new String(respByte,"utf-8").trim());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    @Override
    public void run() {
        while(true){
        }
    }
    public static void main(String[] args) throws Exception {
        for (int i = 0; i < 10; i++) {
            AioSocketClient myClient = new AioSocketClient();
            myClient.connect();
            new Thread(myClient, "myClient").start();
            myClient.write("aaaaaaaaaaaaaaaaaaaaaa");
        }
    }
}