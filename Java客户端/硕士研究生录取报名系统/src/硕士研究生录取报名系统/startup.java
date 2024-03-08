package 硕士研究生录取报名系统;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class startup extends JFrame {
    /**
     *
     */
    private static final long serialVersionUID = 1L;

    public startup()
    {
        setTitle("硕士研究生录取报名系统 V2.0");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.setSize(900,600);
        this.setLocation(550,200);
        JPanel A=new JPanel();
        A.setBackground(Color.WHITE);
        ImageIcon im =new ImageIcon("Pictures/beihua.png");
        JLabel a=new JLabel(im);
        A.add(a);

        JLabel ja=new JLabel("北华大学(西校区)");
        ja.setFont(new Font("楷体",Font.BOLD,40));
        ja.setBounds(100, 400, 400, 150);
        A.add(ja);
        JLabel ja1=new JLabel("硕士研究生录取报名系统");
        ja1.setFont(new Font("楷体",Font.BOLD,40));
        ja1.setBounds(120, 420, 400, 150);
        A.add(ja1);

        JPanel B=new JPanel(new BorderLayout());
        B.setBackground(Color.YELLOW);
        JSplitPane jSplitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT,A,B);//分屏的方式：左右HORIZONTAL_SPLIT，上下VERTICAL_SPLIT
        jSplitPane.setDividerLocation(600);//左边占的长度
        this.add(jSplitPane);
        jSplitPane.setDividerSize(8);//分界线的宽度 设置为0 即不显示出分界线
        A.setBorder(BorderFactory.createLineBorder(Color.BLUE));
        B.setBorder(BorderFactory.createLineBorder(Color.BLUE));

        JLabel w=new JLabel(" 您的身份是 ");

        JButton g=new JButton("管理员");
        JPanel G=new JPanel();
        G.add(g);
        G.setBackground(Color.PINK);
        g.setContentAreaFilled(false);

        JButton d=new JButton("导师");
        JPanel D=new JPanel();
        D.setBackground(Color.PINK);
        D.add(d);
        d.setContentAreaFilled(false);

        JButton x=new JButton("学生");
        JPanel X=new JPanel();
        X.add(x);
        X.setBackground(Color.PINK);
        x.setContentAreaFilled(false);

        
        B.add(w,BorderLayout.NORTH);
        w.setHorizontalAlignment(SwingConstants.CENTER);//居中
        w.setPreferredSize(new Dimension(0,150));//宽度150
        w.setFont(new Font("楷体",Font.PLAIN,25));//设置字体的字体，样子，大小
        B.add(X,BorderLayout.CENTER);
        B.add(D,BorderLayout.SOUTH);

        D.setPreferredSize(new Dimension(0,200));//宽度300

        B.add(G,BorderLayout.NORTH);//B.add(D,BorderLayout.SOUTH);
        G.setPreferredSize(new Dimension(0,150));//宽度300

        g.addActionListener(new ActionListener()    //监听管理员按钮
        {

            public void actionPerformed(ActionEvent e)
            {
                //AdminS admin1 = new AdminS();
                AdminD admin2 = new AdminD();
            }
        });

        x.addActionListener(new ActionListener()    //监听学生按钮
        {

            public void actionPerformed(ActionEvent e)
            {
                new XX();
            }
        });

        d.addActionListener(new ActionListener()   //监听导师按钮
        {
            public void actionPerformed(ActionEvent e)
            {
                new DS();
            }
        });

    }

    public static void main(String[] args)
    {
        new startup().setVisible(true);

    }

}
