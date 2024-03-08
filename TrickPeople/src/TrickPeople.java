

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;


import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JLayeredPane;
import javax.swing.JOptionPane;

public class TrickPeople extends JFrame {

    private static final long serialVersionUID = 1L;





    public TrickPeople(String name) {
        setTitle(name);											//设置窗口标题
        setSize(400, 247);										//设置窗口大小
        setLocationRelativeTo(null);							//设置窗口位置居中
        setResizable(false);									//设置窗口大小不可改变
        setDefaultCloseOperation(DO_NOTHING_ON_CLOSE);
        addWindowListener(new WindowAdapter() {					//给窗口叉号（关闭）增加监听事件
            @Override
            public void windowClosing(WindowEvent e) {
                JOptionPane.showMessageDialog(null,"承认吧，关闭窗口也改变不了的事实！！");
            }
        });
        TrickPeopleView trickPeopleView = new TrickPeopleView();//创建面板对象
        add(trickPeopleView);									//将面板添加到窗口上
        setVisible(true);										//设置窗口可见
    }

    /**
     * 功能:内部类，自定义面板及相应组件的添加
     */
    public class TrickPeopleView extends JLayeredPane {

        private static final long serialVersionUID = 1L;

        private boolean flag = false;
        private int count = 1;

        public TrickPeopleView() {
            setSize(400, 247);
            setFocusable(true);
            setDoubleBuffered(true);
            //添加label标签
            JLabel label = new JLabel();


            label.setSize(400,247);
            label.setLocation(0, 0);
            add(label, new Integer(0));
            //添加两个按钮
            JButton YES = new JButton("我当然是啊");
            YES.setBounds(80, 160, 100, 30);
            YES.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    System.exit(0);
                }
            });
            JButton NO = new JButton("不是");
            NO.setBounds(240, 160, 60, 30);
            NO.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseEntered(MouseEvent e) {
                    if (count%5 != 0) {
                        YES.setLocation(80, 160);
                        NO.setLocation(240, 160);
                        repaint();
                        if (flag) {
                            flag = false;
                            NO.setLocation(240, 160);
                            repaint();
                            count++;
                        }else {
                            flag = true;
                            NO.setLocation(240, 100);
                            repaint();
                        }
                    }else {
                        count = 1;
                        YES.setLocation(240, 160);
                        NO.setLocation(80, 160);
                        repaint();
                        flag = true;
                    }
                }
            });
            JLabel aa=new JLabel("请问你是小懒虫吗？");
            aa.setFont(new Font("楷体",Font.BOLD,18));
            aa.setBounds(80, 50, 270, 30);
            add(aa);

            JLabel bb=new JLabel("@sqt");
            bb.setFont(new Font("楷体",Font.BOLD,18));
            bb.setBounds(340, 180, 270, 30);
            add(bb);
            add(YES, new Integer(1));
            add(NO, new Integer(1));
            setVisible(true);
        }
    }

    public static void main(String[] args) {
        new TrickPeople("送给最好的你");
    }
}