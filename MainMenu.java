import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;

/**
 *
 * Description
 *
 * @version 1.0 from 10/06/2022
 * @author 
 */

public class MainMenu extends JFrame {
  // start attributes
  private JLabel jlb_title = new JLabel("LunarLander", SwingConstants.CENTER);
  private JSeparator jSeparator1 = new JSeparator();
  public JTextField jtf_seed = new JTextField();
  public JTextField jtf_wndw_height = new JTextField();
  public JTextField jtf_wndw_width = new JTextField();
  private JLabel jlb_seed = new JLabel();
  private JLabel jlb_wndw_height = new JLabel();
  private JLabel jlb_wndw_width = new JLabel();
  public JTextField jtf_name = new JTextField();
  public JButton jbtn_play = new JButton();
  private JLabel jlb_name = new JLabel("Enter name:", SwingConstants.CENTER);
  public JButton jbtn_save_settings = new JButton();
  // end attributes
  
  public MainMenu() { 
    // Frame-Init
    super();
    setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    int frameWidth = 320; 
    int frameHeight = 422;
    setSize(frameWidth, frameHeight);
    Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
    int x = (d.width - getSize().width) / 2;
    int y = (d.height - getSize().height) / 2;
    setLocation(x, y);
    setTitle("MainMenu");
    setResizable(false);
    Container cp = getContentPane();
    cp.setLayout(null);
    // start components
    
    jlb_title.setBounds(8, 8, 286, 60);
    jlb_title.setFont(new Font("Arial", Font.BOLD, 42));
    cp.add(jlb_title);
    jSeparator1.setBounds(8, 72, 289, 9);
    cp.add(jSeparator1);
    jtf_seed.setBounds(144, 104, 150, 20);
    cp.add(jtf_seed);
    jtf_wndw_height.setBounds(144, 142, 70, 20);
    cp.add(jtf_wndw_height);
    jtf_wndw_width.setBounds(144, 182, 70, 20);
    cp.add(jtf_wndw_width);
    jlb_seed.setBounds(12, 103, 200, 40);
    jlb_seed.setText("<html>Seed:<br></br>(leave blank for random seed)</html>");
    cp.add(jlb_seed);
    jlb_wndw_height.setBounds(12, 143, 110, 20);
    jlb_wndw_height.setText("Window height:");
    cp.add(jlb_wndw_height);
    jlb_wndw_width.setBounds(12, 183, 110, 20);
    jlb_wndw_width.setText("Window width:");
    cp.add(jlb_wndw_width);
    jtf_name.setBounds(65, 263, 150, 20);
    cp.add(jtf_name);
    jbtn_play.setBounds(10, 299, 283, 65);
    jbtn_play.setText("PLAY");
    jbtn_play.setFont(new Font("Arial", Font.BOLD, 48));
    jbtn_play.setMargin(new Insets(2, 2, 2, 2));
    jbtn_play.addActionListener(new ActionListener() { 
      public void actionPerformed(ActionEvent evt) { 
        jbtn_play_ActionPerformed(evt);
      }
    });
    cp.add(jbtn_play);
    jlb_name.setBounds(56, 240, 166, 20);
    cp.add(jlb_name);
    
    setVisible(true);
    jbtn_save_settings.setText("Save");
    jbtn_save_settings.setMargin(new Insets(2, 2, 2, 2));
    jbtn_save_settings.addActionListener(new ActionListener() { 
      public void actionPerformed(ActionEvent evt) { 
        jbtn_save_settings_ActionPerformed(evt);
      }
    });
    cp.add(jbtn_save_settings);
    jbtn_save_settings.setBounds(216, 160, 83, 25);
    // end components
  } // end of public MainMenu
  
  // start methods
  
  public static void main(String[] args) {
    new MainMenu();  
  } // end of main         
  
  public void jbtn_play_ActionPerformed(ActionEvent evt) {
    // TODO add your code here
    
  } // end of jbtn_play_ActionPerformed

  public void jbtn_save_settings_ActionPerformed(ActionEvent evt) {
    // TODO add your code here
    
  } // end of jbtn_save_settings_ActionPerformed

  // end methods
} // end of class MainMenu
