public class AioSocketServer {
    private ExecutorService executorService;          // Thread pool
    private AsynchronousChannelGroup threadGroup;      // Channel group
    public AsynchronousServerSocketChannel asynServerSocketChannel;  // Server channel
    public void start(Integer port){
        try {
            // 1. Create a cache pool
            executorService = Executors.newCachedThreadPool();
            // 2. Creating Channel Groups
            threadGroup = AsynchronousChannelGroup.withCachedThreadPool(executorService, 1);
            // 3. Create server channels
            asynServerSocketChannel = AsynchronousServerSocketChannel.open(threadGroup);
            // 4. Binding
            asynServerSocketChannel.bind(new InetSocketAddress(port));
            System.out.println("server start , port : " + port);
            // 5. Waiting for Client Request
            asynServerSocketChannel.accept(this, new AioServerHandler());
            // The server is blocked all the time, and the real environment is running under tomcat, so this line of code is not needed.
            Thread.sleep(Integer.MAX_VALUE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        AioSocketServer server = new AioSocketServer();
        server.start(8888);
    }
}
public class AioServerHandler  implements CompletionHandler<AsynchronousSocketChannel, AioSocketServer> {
    private final Integer BUFFER_SIZE = 1024;
    @Override
    public void completed(AsynchronousSocketChannel asynSocketChannel, AioSocketServer attachment) {
        // Ensure that multiple clients can block
        attachment.asynServerSocketChannel.accept(attachment, this);
        read(asynSocketChannel);
    }
    //Read data
    private void read(final AsynchronousSocketChannel asynSocketChannel) {
        ByteBuffer byteBuffer = ByteBuffer.allocate(BUFFER_SIZE);
        asynSocketChannel.read(byteBuffer, byteBuffer, new CompletionHandler<Integer, ByteBuffer>() {
            @Override
            public void completed(Integer resultSize, ByteBuffer attachment) {
                //After reading, reset the identifier bit
                attachment.flip();
                //Get the number of bytes read
                System.out.println("Server -> " + "The length of data received from the client is:" + resultSize);
                //Get the read data
                String resultData = new String(attachment.array()).trim();
                System.out.println("Server -> " + "The data information received from the client is:" + resultData);
                String response = "Server response, Received data from client: " + resultData;
                write(asynSocketChannel, response);
            }
            @Override
            public void failed(Throwable exc, ByteBuffer attachment) {
                exc.printStackTrace();
            }
        });
    }
    // Write data
    private void write(AsynchronousSocketChannel asynSocketChannel, String response) {
        try {
            // Write the data into the buffer
            ByteBuffer buf = ByteBuffer.allocate(BUFFER_SIZE);
            buf.put(response.getBytes());
            buf.flip();
            // Write from buffer to channel
            asynSocketChannel.write(buf).get();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
    }
    @Override
    public void failed(Throwable exc, AioSocketServer attachment) {
        exc.printStackTrace();
    }
}