package 硕士研究生录取报名系统;


import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.sql.*;
import java.util.Vector;

public class XXDL extends JFrame {
    /**
     *
     */
    private static final long serialVersionUID = 1L;
    JTabbedPane jtbp; //定义选项卡
    JPanel jp1,jp2,jp3;	//定义面板

    public XXDL() throws SQLException, ClassNotFoundException
    {
        super("学生登陆");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(900,600);
        this.setLocationRelativeTo(null);
        setVisible(true);

        MenuBar bar = new MenuBar();// 创建菜单栏
        bar.setFont(new Font("楷体",Font.PLAIN,30));
        Menu fileMenu = new Menu("File");// 创建“文件”菜单
        fileMenu.setFont(new Font("楷体",Font.PLAIN,17));
        MenuItem save = new MenuItem("Save All            (Ctrl+S)");
        MenuItem open = new MenuItem("Open");
        MenuItem settings = new MenuItem("Settings         (Ctrl+Alt+S)");
        MenuItem exit = new MenuItem("Exit");
        MenuItem print = new MenuItem("Print                (Ctrl+P)");

        Menu editMenu = new Menu("Edit");// 创建“文件”菜单
        editMenu.setFont(new Font("楷体",Font.PLAIN,17));
        MenuItem undo = new MenuItem("Undo Typing            (Ctrl+Z)");
        MenuItem redo = new MenuItem("Redo");
        Menu help = new Menu("Help");// 创建“帮助"菜单
        help.setFont(new Font("楷体",Font.PLAIN,17));
        MenuItem admin1 = new MenuItem("Shi Qingtian：18294110256");
        MenuItem admin2 = new MenuItem("Chen       Qi：13166961930");
        MenuItem admin3 = new MenuItem("Wu   Bingze：13843747760");

        exit.addActionListener(e -> {
            new XX();
            closeThis();
        });

        fileMenu.add(save);
        fileMenu.addSeparator();// 设置菜单分隔符
        fileMenu.add(print);
        fileMenu.addSeparator();// 设置菜单分隔符
        fileMenu.add(open);
        fileMenu.addSeparator();// 设置菜单分隔符
        fileMenu.add(settings);
        fileMenu.addSeparator();// 设置菜单分隔符
        fileMenu.add(exit);
        editMenu.add(undo);
        editMenu.addSeparator();// 设置菜单分隔符
        editMenu.add(redo);

        help.add(admin1);
        help.add(admin2);
        help.add(admin3);
        bar.add(fileMenu);// 将文件添加到菜单栏上
        bar.add(editMenu);// 将文件添加到菜单栏上
        bar.add(help);// 将文件添加到菜单栏上
        setMenuBar(bar);// 设置菜单栏，使用这种方式设置菜单栏可以不占用布局空间

        //创建组件
        jp1= new JPanel();
        jp2= new JPanel();
        jp3= new JPanel();
        jp1.setBackground(Color.GREEN);
        jp2.setBackground(Color.CYAN);
        jp3.setBackground(Color.ORANGE);


        //jp1面板上上的内容
        String[][] datas = {};
        String[] titles = { "学号", "密码","姓名","性别" };//Sno,Spassword,Sname,Ssex,grade
        String[][] datas1 = {};
        String[] titles1 = { "个人简历"};

        DefaultTableModel myModel  = new DefaultTableModel(datas, titles);// myModel存放表格的数据
        DefaultTableModel myModel1 = new DefaultTableModel(datas1, titles1);
        JTable table  = new JTable(myModel);// 表格对象table的数据来源是myModel对象
        JTable table1 = new JTable(myModel1);
        table.setPreferredScrollableViewportSize(new Dimension(550, 200));// 表格的显示尺寸
        table1.setPreferredScrollableViewportSize(new Dimension(550, 200));
        // 产生一个带滚动条的面板
        JScrollPane scrollPane = new JScrollPane(table);
        JScrollPane scrollPane1 = new JScrollPane(table1);
        //行高
        table.setRowHeight(45);
        table1.setRowHeight(45);

        JLabel t=new JLabel("获奖证书：");
        t.setFont(new Font("楷体",Font.BOLD,20));

        Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
        String url="jdbc:sqlserver://192.168.43.116:1433;DatabaseName=STUDENT_LUQU_BAOMING";
        String user="sa";//sa超级管理员
        String password="12345678";//密码
        Connection conn= DriverManager.getConnection(url,user,password);
        Statement st=conn.createStatement();

        String  strSQL="(Select * from  dbo.Student where Sno='"+ XX.user.getText()+"')";
        ResultSet rs=st.executeQuery(strSQL);
        if(rs.next())
        {
            Vector<String> ve = new Vector<String>();
            ve.addElement(rs.getString(1));
            ve.addElement(rs.getString(2));
            ve.addElement(rs.getString(3));
            ve.addElement(rs.getString(4));
            //ve.addElement(rs.getString(5));
            myModel.addRow(ve);
        }

        String  s1="(Select Sno,Spassword,Sname,Ssex,grade from dbo.student where Sno='"+XX.user.getText()+"')";//+"' And student.Sno=S_C.Sno)";
        ResultSet r1=st.executeQuery(s1);
        if(r1.next())
        {
            String  s2="(Select 个人简介 from dbo.Student where Sno='"+XX.user.getText()+"')";//+"' And Course.Cno=S_C.Cno)";
            ResultSet r2=st.executeQuery(s2);
            while(r2.next())
            {
                Vector<String> ve1 = new Vector<String>();
                ve1.addElement(r2.getString(1));
                //ve1.addElement(r2.getString(2));
                //ve1.addElement(r2.getString(4));
                myModel1.addRow(ve1);
            }
        }

        ImageIcon im1 =new ImageIcon("Pictures/1.png");
        JLabel j=new JLabel(im1);
        ImageIcon im2 =new ImageIcon("Pictures/z.png");
        JLabel j1=new JLabel(im2);

        JButton xiugai=new JButton("修改信息");
        xiugai.setContentAreaFilled(false);
        xiugai.setFont(new Font("楷体",Font.BOLD,14));

        xiugai.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                new XXXG(XX.user.getText());

            }
        });

        JButton again=new JButton("刷新一下");
        again.setContentAreaFilled(false);
        again.setFont(new Font("楷体",Font.BOLD,14));
        again.addActionListener(e -> {
            try {
                Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                String url1 ="jdbc:sqlserver://192.168.43.116:1433;DatabaseName=STUDENT_LUQU_BAOMING";
                String user1 ="student_login";//student登录
                String password1 ="12345678";//密码
                Connection conn1 =DriverManager.getConnection(url1, user1, password1);
                Statement st1 = conn1.createStatement();

                while(myModel1.getRowCount()>0)
                {
                    myModel1.removeRow(myModel1.getRowCount()-1);
                }

                String s11 ="(Select Sno,Spassword,Sname,Ssex,grade from dbo.student where Sno='"+XX.user.getText()+"')";//+"' And student.Sno=S_C.Sno)";
                ResultSet r11 = st1.executeQuery(s11);
                if(r11.next())
                {
                    String  s2="(Select 个人简介,证书图片 from dbo.student where Sno='"+ r11.getString(1)+"')";//+"' And Course.Cno=S_C.Cno)";
                    ResultSet r2= st1.executeQuery(s2);
                    while(r2.next())
                    {
                        Vector<String> ve1 = new Vector<String>();
                        ve1.addElement(r2.getString(1));
                        ve1.addElement(r2.getString(2));
                        //ve1.addElement(r2.getString(4));
                        myModel1.addRow(ve1);
                    }
                    conn1.close();
                }
            }catch (ClassNotFoundException ex) {
                System.out.println("没有找到对应的数据库驱动类");
            }
            catch (SQLException ex) {
                System.out.println("数据库连接或者是数据库操作失败");
            }
        });

        JButton pho=new JButton("上传照片");
        JLabel photo=new JLabel();
        pho.setBounds(490,330,100,30);
        pho.setContentAreaFilled(false);
        photo.setBounds(280,370,150,150);
        jp1.add(pho);
        jp1.add(photo);
        pho.addActionListener(e -> {
            JFileChooser fileChooser = new JFileChooser("Pictures");
            fileChooser.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            int returnVal = fileChooser.showOpenDialog(fileChooser);
            if(returnVal == JFileChooser.APPROVE_OPTION)
            {
                File filePath = fileChooser.getSelectedFile();//获取图片路径
                System.out.println(filePath);
                String f=filePath.getPath();
                String filePath1=f.replaceAll("\\\\", "\\\\\\\\");	//将\转义为\\
                ImageIcon p = new ImageIcon(filePath1);
                photo.setIcon(p);
            }
        });



        //jp2面板上的内容
        String[][] datas2 = {};
        String[] titles2 = { "志愿号", "研究方向","导师" ,"录取人数","奖学金","要求"};
        DefaultTableModel myModel2 = new DefaultTableModel(datas2, titles2);
        JTable table2  = new JTable(myModel2);
        table2.setRowHeight(20);
        table2.setPreferredScrollableViewportSize(new Dimension(550, 200));
        JScrollPane scrollPane2 = new JScrollPane(table2);
        String  s2="(Select * from V_Zhiyuantianbao )";
        ResultSet r2=st.executeQuery(s2);
        while(r2.next())
        {
            Vector<String> ve2 = new Vector<String>();
            ve2.addElement(r2.getString(1));
            ve2.addElement(r2.getString(2));
            ve2.addElement(r2.getString(3));
            ve2.addElement(r2.getString(4));
            ve2.addElement(r2.getString(5));
            ve2.addElement(r2.getString(6));
            myModel2.addRow(ve2);
        }
        conn.close();

        JLabel a=new JLabel("请输入你选择的一志愿代码号：");
        a.setFont(new Font("楷体",Font.BOLD,18));
        JTextField b=new JTextField(20);
        //JButton c=new JButton("确定");
        //c.setFont(new Font("楷体",Font.BOLD,20));

        JLabel aa=new JLabel("请输入你选择的二志愿代码号：");
        aa.setFont(new Font("楷体",Font.BOLD,18));
        JTextField bb=new JTextField(20);
        JButton c=new JButton("确定");
        c.setFont(new Font("楷体",Font.BOLD,20));

        c.addActionListener(e -> {
            try {
                Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                String url12 ="jdbc:sqlserver://192.168.43.116:1433;DatabaseName=STUDENT_LUQU_BAOMING";
                String user12 ="sa";//sa超级管理员
                String password12 ="12345678";//密码
                Connection conn12 =DriverManager.getConnection(url12, user12, password12);
                Statement st12 = conn12.createStatement();

                String ok1=b.getText().trim();
                String ok2=bb.getText().trim();
                String s="(Select * from dbo.Zhiyuan where Zno='"+ok1+"' or Zno='"+ok2+"' )";//
                ResultSet r= st12.executeQuery(s);
                if(r.next())
                {

                    String s112 ="(Select * from dbo.Tianbao where Sno='"+XX.user.getText()+"' )";//+"' And S_C.Sno=student.Sno )";
                    ResultSet r112 = st12.executeQuery(s112);
                    if(r112.next())
                    {
                        String strSQL11 ="update Tianbao set FirstZhiyuan='"+ ok1+"',SecondZhiyuan='"+ok2+"'where Sno='"+XX.user.getText()+"'";
                        int rr11= st12.executeUpdate(strSQL11);
                        if(rr11==1)
                        {
                            JOptionPane.showMessageDialog(null, "志愿填报成功","提示消息",JOptionPane.WARNING_MESSAGE);
                        }
                        else
                        {
                            JOptionPane.showMessageDialog(null, "输入有误~","提示消息",JOptionPane.WARNING_MESSAGE);
                        }
                        /*
                        String s21 ="(Select * from dbo.Tianbao where FirstZhiyuan='"+ ok1+"'  and SecondZhiyuan='"+ok2+"' where Sno='"+XX.user.getText()+"' )";//+"' And Cno='"+ok+"' )";
                        ResultSet r21 = st12.executeQuery(s21);
                        String s22 ="(Select * from dbo.Tianbao where FirstZhiyuan='"+ ok1+"'  or SecondZhiyuan='"+ok2+"' where Sno='"+XX.user.getText()+"' )";//+"' And Cno='"+ok+"' )";
                        ResultSet r22 = st12.executeQuery(s22);
                        if(r21.next())
                        {
                            JOptionPane.showMessageDialog(null, "您的一二志愿已经是这样了！~","提示消息",JOptionPane.WARNING_MESSAGE);
                        }
                        else if(r22.next())
                        {
                            String strSQL11 ="(update Tianbao set FirstZhiyuan='"+ ok1+"',SecondZhiyuan='"+ok2+"'where Sno='"+XX.user.getText()+"')";
                            int rr11= st12.executeUpdate(strSQL11);
                            if(rr11==1)
                            {
                                JOptionPane.showMessageDialog(null, "志愿修改成功","提示消息",JOptionPane.WARNING_MESSAGE);
                            }
                        }
                        else
                        {
                            String ss="(Select * from dbo.Tianbao where Sno='"+XX.user.getText()+"')";
                            ResultSet rr= st12.executeQuery(ss);
                            if(rr.next())
                            {
                                String strSQL1 ="insert into dbo.Tianbao values('"+XX.user.getText()+"','"+ok1+"','"+ok2+"' )";
                                int rr1= st12.executeUpdate(strSQL1);
                                if(rr1==1)
                                {
                                    JOptionPane.showMessageDialog(null, "志愿填报成功","提示消息",JOptionPane.WARNING_MESSAGE);
                                }else{JOptionPane.showMessageDialog(null, "您的一二志愿已经是这样了！~","提示消息",JOptionPane.WARNING_MESSAGE);}
                            }
                        }*/
                    }
                    else
                    {
                        String strSQL1 ="insert into dbo.Tianbao values('"+XX.user.getText()+"','"+ok1+"','"+ok2+"' )";
                        ResultSet rr1= st12.executeQuery(strSQL1);
                        if(rr1.next())
                        {
                            JOptionPane.showMessageDialog(null, "志愿填报成功","提示消息",JOptionPane.WARNING_MESSAGE);
                        }}
                }
                else
                {
                    JOptionPane.showMessageDialog(null, "志愿代码可能有误哦~","提示消息",JOptionPane.WARNING_MESSAGE);
                }
                conn12.close();

            }catch (ClassNotFoundException ex) {
                System.out.println("没有找到对应的数据库驱动类");
            }
            catch (SQLException ex) {
                //System.out.println("数据库连接或者是数据库操作失败XXDL3");
            }
        });




        //jp3上的内容
        String[][] datas3 = {};
        String[] titles3 = { "研究方向", "导师姓名","导师性别","联系电话","奖学金" };
        DefaultTableModel myModel3  = new DefaultTableModel(datas3, titles3);// myModel存放表格的数据
        JTable table3  = new JTable(myModel3);// 表格对象table的数据来源是myModel对象
        table3.setPreferredScrollableViewportSize(new Dimension(550, 100));// 表格的显示尺寸
        // 产生一个带滚动条的面板
        JScrollPane scrollPane3 = new JScrollPane(table3);
        //行高
        table3.setRowHeight(20);

        ImageIcon im3 =new ImageIcon("Pictures/3.png");
        JLabel j2=new JLabel(im3);
        JLabel ja1=new JLabel("金榜题名，还看今朝");
        JLabel ja2=new JLabel("您的成绩是：");
        JLabel ja3=new JLabel("录取结果：");
        JLabel ja4=new JLabel("(单击查询哦~)");
        ja1.setFont(new Font("楷体",Font.BOLD,40));
        ja2.setFont(new Font("楷体",Font.BOLD,20));
        ja3.setFont(new Font("楷体",Font.BOLD,20));
        ja4.setFont(new Font("楷体",Font.BOLD,15));
        JTextField b1=new JTextField(15);
        JTextField b2=new JTextField(15);
        //JTextField b3=new JTextField(15);
        JButton c1=new JButton("查 询");

        c1.addActionListener(e -> {
            try {
                Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                String url13 ="jdbc:sqlserver://192.168.43.116:1433;DatabaseName=STUDENT_LUQU_BAOMING";
                String user13 ="sa";//sa超级管理员
                String password13 ="12345678";//密码
                Connection conn13 =DriverManager.getConnection(url13, user13, password13);
                Statement st13 = conn13.createStatement();

                String  strSQL3="(Select * from  V_Daoshizhuanyexinxi where  Sno='"+ XX.user.getText()+"')";
                ResultSet rs3=st13.executeQuery(strSQL3);



                if(rs3.next())
                {
                    Vector<String> ve3 = new Vector<String>();
                    ve3.addElement(rs3.getString(1));
                    ve3.addElement(rs3.getString(2));
                    ve3.addElement(rs3.getString(3));
                    ve3.addElement(rs3.getString(4));
                    ve3.addElement(rs3.getString(5));
                    myModel3.addRow(ve3);
                    b2.setText(rs3.getString(6));

                }
                else
                {
                    JOptionPane.showMessageDialog(null, "很遗憾哦，你落榜了，明年再来吧~","提示消息",JOptionPane.WARNING_MESSAGE);
                }
                conn13.close();

                /*String B1=b1.getText().trim();
                String L="(Select * from dbo.student where Sno='"+XX.user.getText()+"')";//+"' And Cno='"+B1+"' And S_C.Sno=student.Sno )";
                ResultSet M= st13.executeQuery(L);
                if(M.next()||rs3.next())
                {

                    //b3.setText(M.getString(2));
                    Vector<String> ve3 = new Vector<String>();
                    ve3.addElement(rs3.getString(1));
                    ve3.addElement(rs3.getString(2));
                    ve3.addElement(rs3.getString(3));
                    ve3.addElement(rs3.getString(4));
                    ve3.addElement(rs3.getString(5));
                    myModel3.addRow(ve3);
                    b2.setText(M.getString(5));
                }
                else
                {
                    JOptionPane.showMessageDialog(null, "落榜哦~","提示消息",JOptionPane.WARNING_MESSAGE);
                }
                conn13.close();*/

            }catch (ClassNotFoundException ex) {
                System.out.println("没有找到对应的数据库驱动类");
            }
            catch (SQLException ex) {
                System.out.println("数据库连接或者是数据库操作失败");
            }
        });


        jp1.setLayout(null);//自由布局
        jp2.setLayout(null);//自由布局
        jp3.setLayout(null);//自由布局

        //jp1中组件的位置
        scrollPane.setBounds(50, 190, 550, 65);
        scrollPane1.setBounds(50, 260, 550, 65);
        j.setBounds(250, 20, 150, 150);
        j1.setBounds(180, 370, 300, 150);
        again.setBounds(490, 140, 100, 30);
        xiugai.setBounds(50, 140, 100, 30);

        t.setBounds(50, 320, 270, 30);


        //jp2中组件的位置
        scrollPane2.setBounds(50, 20, 550, 400);
        a.setBounds(50, 430, 270, 30);
        b.setBounds(320, 430, 150, 25);
        //c.setBounds(500, 430, 80, 27);

        aa.setBounds(50, 470, 270, 30);
        bb.setBounds(320, 470, 150, 25);
        c.setBounds(500, 470, 80, 27);


        //jp3中组件的位置
        j2.setBounds(430, 130, 200, 180);
        ja1.setBounds(50, 50, 400, 150);
        ja2.setBounds(80, 220, 150, 30);
        ja3.setBounds(80, 270, 150, 30);
        ja4.setBounds(435, 80, 150, 30);
        //b1.setBounds(260, 50, 150, 25);
        b2.setBounds(260, 220, 100, 25);
        //b3.setBounds(260, 270, 100, 25);
        c1.setBounds(450, 50, 70, 30);

        scrollPane3.setBounds(30, 320, 550, 200);

        // 将组件添加入jp1窗口中
        jp1.add(scrollPane);
        jp1.add(scrollPane1);
        jp1.add(j);
        jp1.add(j1);
        jp1.add(again);
        jp1.add(xiugai);

        jp1.add(t);

        // 将组件添加入jp2窗口中
        jp2.add(scrollPane2);
        jp2.add(a);
        jp2.add(b);
        jp2.add(c);
        jp2.add(aa);
        jp2.add(bb);
        //jp2.add(cc);

        // 将组件添加入jp3窗口中
        jp3.add(j2);
        jp3.add(ja1);
        jp3.add(ja2);
        jp3.add(ja3);
        jp3.add(ja4);
        //jp3.add(b1);
        jp3.add(b2);
        //jp3.add(b3);
        jp3.add(c1);

        jp3.add(scrollPane3);

        jtbp=new JTabbedPane(JTabbedPane.LEFT); //创建选项卡并使选项卡垂直排列
        jtbp.add("个人信息",jp1);
        jtbp.add("志愿填报",jp2);
        jtbp.add("录取结果查询",jp3);
        jtbp.setFont(new Font("楷体",Font.PLAIN,30));
        this.add(jtbp);    //添加选项卡窗格到容器
    }

    public  void closeThis()//关闭当前界面
    {
        this.dispose();
    }
}

