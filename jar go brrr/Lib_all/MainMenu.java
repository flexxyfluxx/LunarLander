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
  public JButton jbtn_hof = new JButton();
  private JSeparator jSeparator2 = new JSeparator();
  private JLabel jLabel6 = new JLabel();
  private JLabel jlb_controls1 = new JLabel();
  private JLabel jlb_controls2 = new JLabel();
  // end attributes
  
  public MainMenu() { 
    // Frame-Init
    super();
    setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    int frameWidth = 318; 
    int frameHeight = 558;
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
    jtf_name.setBounds(65, 234, 150, 20);
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
    jlb_name.setBounds(56, 211, 166, 20);
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
    jbtn_hof.setBounds(84, 264, 115, 25);
    jbtn_hof.setText("Hall of Fame");
    jbtn_hof.setMargin(new Insets(2, 2, 2, 2));
    jbtn_hof.addActionListener(new ActionListener() { 
      public void actionPerformed(ActionEvent evt) { 
        jbtn_hof_ActionPerformed(evt);
      }
    });
    cp.add(jbtn_hof);
    jSeparator2.setBounds(8, 368, 281, 9);
    cp.add(jSeparator2);
    jLabel6.setBounds(90, 382, 110, 23);
    jLabel6.setText("text");
    jLabel6.setFont(new Font("Arial", Font.BOLD, 16));
    jLabel6.setHorizontalTextPosition(SwingConstants.CENTER);
    jLabel6.setHorizontalAlignment(SwingConstants.CENTER);
    cp.add(jLabel6);
    jlb_controls1.setBounds(19, 413, 100, 92);
    jlb_controls1.setText("<html>Thrust Up:<br>Thrust Down:<br>Rotate Left:<br>Rotate Right:<br>Max Thrust:<br>Min Thrust:</html>");
    cp.add(jlb_controls1);
    jlb_controls2.setBounds(170, 413, 100, 92);
    jlb_controls2.setText("<html>W<br>S<br>A<br>D<br>E<br>Q</html>");
    jlb_controls2.setHorizontalAlignment(SwingConstants.LEFT);
    jlb_controls2.setHorizontalTextPosition(SwingConstants.RIGHT);
    cp.add(jlb_controls2);
    jLabel6.setText("Controls");
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

  public void jbtn_hof_ActionPerformed(ActionEvent evt) {
    // TODO add your code here
    
  } // end of jbtn_hof_ActionPerformed     

  // end methods
} // end of class MainMenu
