import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;

/**
 *                               
 * Description                   
 *                               
 * @version 1.0 from 20/06/2022  
 * @author                       
 */

public class Leaderboard extends JFrame {
  // start attributes
  public JTextArea jta_top_scores = new JTextArea("test");
    private JScrollPane jTextArea1ScrollPane = new JScrollPane(jta_top_scores);
  public JTextArea jta_top_players = new JTextArea("test");
    private JScrollPane jTextArea2ScrollPane = new JScrollPane(jta_top_players);
  private JSeparator jSeparator1 = new JSeparator(SwingConstants.VERTICAL);
  private JLabel jLabel1 = new JLabel("TOP SCORES", SwingConstants.CENTER);
  private JLabel jLabel2 = new JLabel("TOP PLAYERS", SwingConstants.CENTER);
  // end attributes
  
  public Leaderboard() { 
    // Frame-Init
    super();
    setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
    int frameWidth = 615; 
    int frameHeight = 637;
    setSize(frameWidth, frameHeight);
    Dimension d = Toolkit.getDefaultToolkit().getScreenSize();
    int x = (d.width - getSize().width) / 2;
    int y = (d.height - getSize().height) / 2;
    setLocation(x, y);
    setTitle("Leaderboard");
    setResizable(false);
    Container cp = getContentPane();
    cp.setLayout(null);
    // start components
    
    jta_top_scores.setFont(new Font("Courier New", Font.PLAIN, 14));
    jta_top_scores.setEditable(false);
    jta_top_players.setFont(new Font("Courier New", Font.PLAIN, 14));
    jta_top_players.setEditable(false);
    jTextArea1ScrollPane.setBounds(0, 64, 300, 536);
    cp.add(jTextArea1ScrollPane);
    jTextArea2ScrollPane.setBounds(300, 64, 300, 536);
    cp.add(jTextArea2ScrollPane);
    jSeparator1.setBounds(299, 1, 4, 64);
    cp.add(jSeparator1);
    jLabel1.setBounds(0, 0, 300, 60);
    jLabel1.setFont(new Font("Arial", Font.BOLD, 32));
    cp.add(jLabel1);
    jLabel2.setBounds(300, 0, 300, 60);  
    jLabel2.setFont(new Font("Arial", Font.BOLD, 32));
    cp.add(jLabel2);
    // end components
    
  } // end of public Leaderboard
  
  // start methods
  
  public static void main(String[] args) {
    new Leaderboard().setVisible(true);
  } // end of main
  
  public void updateBoards(String playerBoard, String scoreBoard) {
    jta_top_scores.setText(scoreBoard);
    jta_top_players.setText(playerBoard);
  }

  
  // end methods
} // end of class Leaderboard
