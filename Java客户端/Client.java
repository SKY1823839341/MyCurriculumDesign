import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Scanner;

public class Client {
    private PrintWriter out;
    //private BufferedReader br;
    private Scanner scan;
    private Boolean flag=true;
    private Socket s;
    private InputStream is;

    public Client() throws UnknownHostException, IOException {

            s=new Socket("192.168.31.26", 2021);
            is=s.getInputStream();
    }

    public static void main(String []args) throws UnknownHostException, IOException {
        try{
            Client client =new Client();
            client.startup();
        }catch(Exception e){
            System.out.println("未找到该服务器！或请检查ip地址与端口是否正确^_^");

        }

    }
    public void startup() throws UnknownHostException, IOException {
        out = new PrintWriter(s.getOutputStream(), true);

        //开启一个线程监听服务端的消息
        Thread ct=new Thread(new Runnable() {

            public void run() {
                while(true) {
                    if(!flag) break;
                    try {
                        receive();
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                }
            }
        });
        ct.start();
        //主线程负责发送消息
        System.out.println("服务器已连接成功，请输入您的群聊昵称：");
        scan = new Scanner(System.in);
        String name=scan.nextLine();
        out.println(name);
        System.out.println("》》 "+name+"，欢迎您进入群聊，输入quit退出群聊《《");
        while(flag) {
            String read=scan.nextLine();
            if(read.equalsIgnoreCase("quit")) {
                flag=false;
            }
            //System.out.println(read);
            out.println(read);
        }
        s.close();
    }

    public void receive() throws IOException {

            try {
                byte ss[] = new byte[1024];
                int length = s.getInputStream().read(ss);
                System.out.println(new String(ss, 0, length));
            } catch (Exception e) {
                System.out.println("连接已断开，可尝试重新连接^…^");
            }

    }
}