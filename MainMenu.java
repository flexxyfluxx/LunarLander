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
  private JLabel jlb_title = new JLabel();
  private JSeparator jSeparator1 = new JSeparator();
  public JTextField jtf_seed = new JTextField();
  public JTextField jtf_wndw_height = new JTextField();
  public JTextField jtf_wndw_width = new JTextField();
  private JLabel jlb_seed = new JLabel();
  private JLabel jlb_wndw_height = new JLabel();
  private JLabel jlb_wndw_width = new JLabel();
  public JTextField jtf_name = new JTextField();
  public JButton jbtn_play = new JButton();
  private JLabel jlb_name = new JLabel();
  // end attributes
  
  public MainMenu() { 
    // Frame-Init
    super();
    setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    int frameWidth = 319; 
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
    jlb_title.setText("LunarLander");
    cp.add(jlb_title);
    jSeparator1.setBounds(8, 72, 289, 9);
    cp.add(jSeparator1);
    jtf_seed.setBounds(144, 104, 150, 20);
    cp.add(jtf_seed);
    jtf_wndw_height.setBounds(144, 141, 70, 20);
    cp.add(jtf_wndw_height);
    jtf_wndw_width.setBounds(144, 184, 70, 20);
    cp.add(jtf_wndw_width);
    jlb_seed.setBounds(12, 103, 110, 20);
    jlb_seed.setText("Seed: (leave blank for random seed)");
    cp.add(jlb_seed);
    jlb_wndw_height.setBounds(12, 143, 110, 20);
    jlb_wndw_height.setText("text");
    cp.add(jlb_wndw_height);
    jlb_wndw_width.setBounds(12, 183, 110, 20);
    jlb_wndw_width.setText("text");
    cp.add(jlb_wndw_width);
    jtf_name.setBounds(65, 263, 150, 20);
    cp.add(jtf_name);
    jbtn_play.setBounds(10, 299, 283, 65);
    jbtn_play.setText("PLAY");
    jbtn_play.setMargin(new Insets(2, 2, 2, 2));
    jbtn_play.addActionListener(new ActionListener() { 
      public void actionPerformed(ActionEvent evt) { 
        jbtn_play_ActionPerformed(evt);
      }
    });
    cp.add(jbtn_play);
    jlb_name.setBounds(56, 216, 166, 36);
    jlb_name.setText("text");
    cp.add(jlb_name);
    jTextField2.setBounds(144, 149, 70, 20);
    jTextField3.setBounds(144, 192, 70, 20);
    jLabel3.setBounds(12, 151, 110, 20);
    jLabel4.setBounds(12, 191, 110, 20);
    jTextField4.setBounds(65, 271, 150, 20);
    jLabel5.setBounds(56, 224, 166, 36);
    jLabel2.setBounds(12, 103, 118, 36);
    // end components
    
    setVisible(true);
  } // end of public MainMenu
  
  // start methods
  
  public static void main(String[] args) {
    new MainMenu();
  } // end of main
  
  public void jbtn_play_ActionPerformed(ActionEvent evt) {
    // TODO add your code here
    
  } // end of jbtn_play_ActionPerformed

  // end methods
} // end of class MainMenu
