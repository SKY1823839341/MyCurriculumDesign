package 硕士研究生录取报名系统;


import javafx.event.ActionEvent;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.UnsupportedEncodingException;
import java.security.NoSuchAlgorithmException;
import java.sql.*;

public class XXZC extends JFrame {
    /**
     *
     */
    private static final long serialVersionUID = 1L;
    private ValidCode vcode = new ValidCode();
    JTextField user,pass,idd,ph,co;
    JButton pho,register,exit;

    public XXZC()
    {
        super("注册");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(500,500);
        this.setLocationRelativeTo(null); //此窗口将置于屏幕的中央
        setVisible(true);

        JPanel frame=new JPanel();
        frame.setBackground(Color.PINK);
        this.add(frame);

        JLabel username=new JLabel("*账号");
        JLabel password=new JLabel("*密码");
        JLabel id=new JLabel("姓名");
        JLabel phone=new JLabel("性别 ");
        JLabel code=new JLabel("*验证码");
        JLabel photo=new JLabel();
        user=new JTextField();
        pass=new JTextField();
        idd=new JTextField();
        ph=new JTextField();
        co=new JTextField();
        pho=new JButton("上传照片");
        register=new JButton("注  册");
        exit=new JButton("退  出");

        username.setBounds(58, 46, 60, 40);
        username.setFont(new Font("楷体",Font.BOLD,17));
        user.setBounds(104,50,120,30);
        password.setBounds(54,100,120,30);
        password.setFont(new Font("楷体",Font.BOLD,17));
        pass.setBounds(104,100,120,30);
        id.setBounds(54,150,120,30);
        id.setFont(new Font("楷体",Font.BOLD,17));
        idd.setBounds(104,150,120,30);
        phone.setBounds(56,200,60,40);
        phone.setFont(new Font("楷体",Font.BOLD,17));
        ph.setBounds(104,200,120,30);
        code.setBounds(41,250,120,30);
        code.setFont(new Font("楷体",Font.BOLD,17));
        co.setBounds(104,250,120,30);
        vcode.setBounds(112, 300, 100, 40);
        photo.setBounds(280,100,150,150);
        pho.setBounds(305,280,100,30);
        pho.setContentAreaFilled(false);
        register.setBounds(150,380,70,30);
        exit.setBounds(250,380,70,30);


        frame.setLayout(null);
        frame.add(username);
        frame.add(user);
        frame.add(password);
        frame.add(pass);
        frame.add(id);
        frame.add(idd);
        frame.add(phone);
        frame.add(ph);
        frame.add(code);
        frame.add(co);
        frame.add(photo);
        frame.add(pho);
        frame.add(register);
        frame.add(exit);
        frame.add(vcode);


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

        register.addActionListener(e -> {
            String user1=user.getText().trim();
            String pass1=pass.getText().trim();
            String id1=idd.getText().trim();
            String ph1=ph.getText().trim();
            String co1=co.getText();

            try {
                Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
                String url="jdbc:sqlserver://192.168.43.116:1433;DatabaseName=STUDENT_LUQU_BAOMING";
                String user="sa";//sa超级管理员
                String password1 ="12345678";//密码
                Connection conn= DriverManager.getConnection(url,user, password1);
                Statement st=conn.createStatement();

                String  strSQL="(select * from  dbo.Student where Sno='"+user1+"' )";
                ResultSet rs=st.executeQuery(strSQL);



                if(co1.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "请输入验证码!","提示消息",JOptionPane.WARNING_MESSAGE);
                }
                else
                {
                    if(!isValidCodeRight()) {
                        JOptionPane.showMessageDialog(null, "验证码错误,请重新输入!","提示消息",JOptionPane.WARNING_MESSAGE);
                    }
                    else {

                        if(rs.next())
                        {
                            JOptionPane.showMessageDialog(null,"该学号已被注册！","温馨提示!", JOptionPane.ERROR_MESSAGE);
                        }
                        else
                        {
                            String sql = "insert into dbo.Student(Sno,Spassword,Sname,Ssex) values('"+user1+"','"+pass1+"','"+id1+"','"+ph1+"') ";
                            PreparedStatement pst = conn.prepareStatement(sql,Statement.RETURN_GENERATED_KEYS);
                            pst.executeUpdate();
                            pst.close();
                            JOptionPane.showMessageDialog(null,"注册成功");
                        }
                        conn.close();
                        //关闭数据库连接
                    }
                }
            }
            catch (ClassNotFoundException ex) {
                System.out.println("没有找到对应的数据库驱动类");
            }
            catch (SQLException ex) {
                System.out.println("数据库连接或者是数据库操作失败");
            }

        });

        exit.addActionListener(e -> {
            closeThis();
            new XX();
        });
    }
    public boolean isValidCodeRight() {

        if(co == null) {
            return false;
        }else if(vcode == null) {
            return true;
        }else if(vcode.getCode() .equals(co.getText())) {
            return true;
        }else
            return false;

    }


    public  void closeThis()//关闭当前界面
    {
        this.dispose();
    }

}
