from gpanel import *
from javax.swing import JFileChooser
from java.io import File
import os
import ntpath

def set_bit(value, bit):
    return value | (1<<bit)

def main():
    fileChooser = JFileChooser()
    fileChooser.setCurrentDirectory(File(os.getcwd()))
    result = fileChooser.showOpenDialog(None)
    if result == JFileChooser.APPROVE_OPTION:
         path = str(fileChooser.getSelectedFile())
    else:
        print "Operation canceled"
        return
    dir, fname =  ntpath.split(os.path.splitext(path)[0])
    img = getImage(path)
    if img == None:
        print "Illegal BMP image file."
        return
    w = img.getWidth()
    h = img.getHeight()
    if w != 128 or h != 64:
        print "Illegal image size. Must be 128 x 64"
        return
    makeGPanel(Size(128, 64))
    window(0, 128, 64, 0)    # y axis downwards
    image(img, 0, 64)
    li = []
    for i in range(8):
        for k in range(128):
            b = 0
            for z in range(8):
                x = k
                y = 8 * i + z
                color = img.getPixelColor(x, y)
                red = color.getRed()
                green = color.getGreen()
                blue = color.getBlue()
                intensity = (red + green + blue) // 3
                if intensity < 100:
                    b = set_bit(b, z)
            li.append(b)
    
    out = os.path.join(dir, fname)
    with open(out, 'wb') as f:
        f.write(bytearray(li))
    print(out + " successfully created.")
    
main()    
