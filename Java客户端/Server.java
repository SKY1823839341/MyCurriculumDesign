import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.text.*;
import java.util.*;



class Server {
    private static List<ThreadServer> clients=new ArrayList<ThreadServer>();



    public void startup() throws IOException {
        System.out.println("正在监听2021端口");
        ServerSocket ss=new ServerSocket(2021);
            while(true){
             //   private PrintWriter out;
             //  private Scanner scan;
             //   scan = new Scanner(System.in);
             //   String read=scan.nextLine();
            //    out.println(read);
              /* BufferedReader buffer = null;
                String messages=buffer.readLine();
                System.out.println(">Server<: "+messages);
                //send(">Server<: "+messages);*/

                try{
                Socket socket=ss.accept();
                System.out.println("有新用户正在尝试连接。。。。。。");
                Thread st=new Thread(new ThreadServer(socket));
                st.start();
                }catch(Exception e){
                    System.out.println("该客户端已强制断开");
        }

    }
    }

    public static class ThreadServer implements Runnable{
        private Socket socket;
        private BufferedReader br;
        private PrintWriter out;
        private String name;
        private Boolean flag=true;
        public ThreadServer(Socket socket) throws IOException {
            this.socket=socket;
            br=new BufferedReader(new InputStreamReader(socket.getInputStream()));
            out=new PrintWriter(socket.getOutputStream(),true);
            String str=br.readLine();
            name=str+"["+socket.getInetAddress().getHostAddress()+":"+socket.getPort()+"]";
            System.out.println(">"+name+"<加入了本群。");
            send(">"+name+"<加入了本群");
            clients.add(this);
        }
        //private
        public void send(String message) {
            try{
                for (ThreadServer threadServer : clients) {
                    //System.out.println("-->已向线程"+threadServer.name+"发送消息");
                    threadServer.out.print(message);
                    threadServer.out.flush();
                }
            }catch(Exception e){
                System.out.println("错误地带八");
            }
        }
        private void receive() throws IOException {

            String message;
            while(flag=true) {
                message=br.readLine();
                if(message.equalsIgnoreCase("quit")) {
                    System.out.println("用户>"+name+"<已退出群聊");
                    //out.println("quit");
                    out.flush();
                    clients.remove(this);
                    flag=false;
                }
                    System.out.print("消息接收时间: ");
                    SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                    System.out.println(df.format(new Date()));
                    System.out.println(">"+name+"<: "+message);
                send(">"+name+"<: "+message);
            }


        }
        public void run() {
            try {
                while(flag=true) {
                    receive();
                }
            } catch (IOException e) {
                e.printStackTrace();
                System.out.println("错误地带六");
            }finally {
                try {
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                    System.out.println("错误地带七");
                }
            }
        }

    }

    public static void main(String []args) throws IOException {

        try{
            Server server=new Server();
            System.out.print("服务器已打开，");
            server.startup();
        }catch(Exception e){
            System.out.println("服务器开启失败，请重试^…^");
        }
    }

}