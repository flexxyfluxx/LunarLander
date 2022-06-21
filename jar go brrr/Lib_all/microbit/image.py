# image.py
# Version 1.00 - July 2, 2018

_HEART = [
    0,1,0,1,0,
    1,1,1,1,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,0,1,0,0]

_SMILE = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,0,0,0,
    1,0,0,0,1,
    0,1,1,1,0]

_HEART_SMALL = [
    0,0,0,0,0,
    0,1,0,1,0,
    0,1,1,1,0,
    0,0,1,0,0,
    0,0,0,0,0]

_HAPPY = [
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    1,0,0,0,1,
    0,1,1,1,0]

_SAD = [
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    0,1,1,1,0,
    1,0,0,0,1]

_CONFUSED = [
    0,0,0,0,0,
    0,1,0,1,0,
    0,0,0,0,0,
    0,1,0,1,0,
    1,0,1,0,1]

_ANGRY = [
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,0,0,0,
    1,1,1,1,1,
    1,0,1,0,1]

_ASLEEP = [
    0,0,0,0,0,
    1,1,0,1,1,
    0,0,0,0,0,
    0,1,1,1,0,
    0,0,0,0,0]

_SURPRISED = [
    0,1,0,1,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    0,0,1,0,0]

_SILLY = [
    1,0,0,0,1,
    0,0,0,0,0,
    1,1,1,1,1,
    0,0,1,0,1,
    0,0,1,1,1]

_FABULOUS = [
    1,1,1,1,1,
    1,1,0,1,1,
    0,0,0,0,0,
    0,1,0,1,0,
    0,1,1,1,0]

_MEH = [
    0,1,0,1,0,
    0,0,0,0,0,
    0,0,0,1,0,
    0,0,1,0,0,
    0,1,0,0,0]

_YES = [
    0,0,0,0,0,
    0,0,0,0,1,
    0,0,0,1,0,
    1,0,1,0,0,
    0,1,0,0,0]

_NO = [
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1]

_CLOCK12 = [
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK1 = [
    0,0,0,1,0,
    0,0,0,1,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK2 = [
    0,0,0,0,0,
    0,0,0,1,1,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK3 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,1,1,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK4 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,1,1,
    0,0,0,0,0]

_CLOCK5 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,0,1,0,
    0,0,0,1,0]

_CLOCK6 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0]

_CLOCK7 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,0,0,
    0,1,0,0,0]

_CLOCK8 = [
    0,0,0,0,0,
    0,0,0,0,0,
    0,0,1,0,0,
    1,1,0,0,0,
    0,0,0,0,0]

_CLOCK9 = [
    0,0,0,0,0,
    0,0,0,0,0,
    1,1,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK10 = [
    0,0,0,0,0,
    1,1,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_CLOCK11 = [
    0,1,0,0,0,
    0,1,0,0,0,
    0,0,1,0,0,
    0,0,0,0,0,
    0,0,0,0,0]

_ARROW_N = [
    0,0,1,0,0,
    0,1,1,1,0,
    1,0,1,0,1,
    0,0,1,0,0,
    0,0,1,0,0]

_ARROW_NE = [
    0,0,1,1,1,
    0,0,0,1,1,
    0,0,1,0,1,
    0,1,0,0,0,
    1,0,0,0,0]

_ARROW_E = [
    0,0,1,0,0,
    0,0,0,1,0,
    1,1,1,1,1,
    0,0,0,1,0,
    0,0,1,0,0]

_ARROW_SE = [
    1,0,0,0,0,
    0,1,0,0,0,
    0,0,1,0,1,
    0,0,0,1,1,
    0,0,1,1,1]

_ARROW_S = [
    0,0,1,0,0,
    0,0,1,0,0,
    1,0,1,0,1,
    0,1,1,1,0,
    0,0,1,0,0]

_ARROW_SW = [
    0,0,0,0,1,
    0,0,0,1,0,
    1,0,1,0,0,
    1,1,0,0,0,
    1,1,1,0,0]

_ARROW_W = [
    0,0,1,0,0,
    0,1,0,0,0,
    1,1,1,1,1,
    0,1,0,0,0,
    0,0,1,0,0]

_ARROW_NW = [
    1,1,1,0,0,
    1,1,0,0,0,
    1,0,1,0,0,
    0,0,0,1,0,
    0,0,0,0,1]

_TRIANGLE = [
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    1,1,1,1,1,
    0,0,0,0,0]

_TRIANGLE_LEFT = [
    1,0,0,0,0,
    1,1,0,0,0,
    1,0,1,0,0,
    1,0,0,1,0,
    1,1,1,1,1]

_CHESSBOARD = [
    0,1,0,1,0,
    1,0,1,0,1,
    0,1,0,1,0,
    1,0,1,0,1,
    0,1,0,1,0]

_DIAMOND = [
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1,
    0,1,0,1,0,
    0,0,1,0,0]

_DIAMOND_SMALL = [
    0,0,0,0,0,
    0,0,1,0,0,
    0,1,0,1,0,
    0,0,1,0,0,
    0,0,0,0,0]

_SQUARE = [
    1,1,1,1,1,
    1,0,0,0,1,
    1,0,0,0,1,
    1,0,0,0,1,
    1,1,1,1,1]

_SQUARE_SMALL = [
    0,0,0,0,0,
    0,1,1,1,0,
    0,1,0,1,0,
    0,1,1,1,0,
    0,0,0,0,0]

_RABBIT = [
    1,0,1,0,0,
    1,0,1,0,0,
    1,1,1,1,0,
    1,1,0,1,0,
    1,1,1,1,0]

_COW = [
    1,0,0,0,1,
    1,0,0,0,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,0,1,0,0]

_MUSIC_CROTCHET = [
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    1,1,1,0,0,
    1,1,1,0,0]

_MUSIC_QUAVER = [
    0,0,1,0,0,
    0,0,1,1,0,
    0,0,1,0,1,
    1,1,1,0,0,
    1,1,1,0,0]

_MUSIC_QUAVERS = [
    0,1,1,1,1,
    0,1,0,0,1,
    0,1,0,0,1,
    1,1,0,1,1,
    1,1,0,1,1]

_PITCHFORK = [
    1,0,1,0,1,
    1,0,1,0,1,
    1,1,1,1,1,
    0,0,1,0,0,
    0,0,1,0,0]

_XMAS = [
    0,0,1,0,0,
    0,1,1,1,0,
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,1,1,1]

_PACMAN = [
    0,1,1,1,1,
    1,1,0,1,0,
    1,1,1,0,0,
    1,1,1,1,0,
    0,1,1,1,1]

_TARGET = [
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,0,1,1,
    0,1,1,1,0,
    0,0,1,0,0]

_TSHIRT = [
    1,1,0,1,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,1,1,1,0,
    0,1,1,1,0]

_ROLLERSKATE = [
    0,0,0,1,1,
    0,0,0,1,1,
    1,1,1,1,1,
    1,1,1,1,1,
    0,1,0,1,0]

_DUCK = [
    0,1,1,0,0,
    1,1,1,0,0,
    0,1,1,1,1,
    0,1,1,1,0,
    0,0,0,0,0]

_HOUSE = [
    0,0,1,0,0,
    0,1,1,1,0,
    1,1,1,1,1,
    0,1,1,1,0,
    0,1,0,1,0]

_TORTOISE = [
    0,0,0,0,0,
    0,1,1,1,0,
    1,1,1,1,1,
    0,1,0,1,0,
    0,0,0,0,0]

_BUTTERFLY = [
    1,1,0,1,1,
    1,1,1,1,1,
    0,0,1,0,0,
    1,1,1,1,1,
    1,1,0,1,1]

_STICKFIGURE = [
    0,0,1,0,0,
    1,1,1,1,1,
    0,0,1,0,0,
    0,1,0,1,0,
    1,0,0,0,1]

_GHOST = [
    1,1,1,1,1,
    1,0,1,0,1,
    1,1,1,1,1,
    1,1,1,1,1,
    1,0,1,0,1]

_SWORD = [
    0,0,1,0,0,
    0,0,1,0,0,
    0,0,1,0,0,
    0,1,1,1,0,
    0,0,1,0,0]

_GIRAFFE = [
    1,1,0,0,0,
    0,1,0,0,0,
    0,1,0,0,0,
    0,1,1,1,0,
    0,1,0,1,0]

_SKULL = [
    0,1,1,1,0,
    1,0,1,0,1,
    1,1,1,1,1,
    0,1,1,1,0,
    0,1,1,1,0]

_UMBRELLA = [
    0,1,1,1,0,
    1,1,1,1,1,
    0,0,1,0,0,
    1,0,1,0,0,
    0,1,1,0,0]

_SNAKE = [
    1,1,0,0,0,
    1,1,0,1,1,
    0,1,0,1,0,
    0,1,1,1,0,
    0,0,0,0,0]

class Image:
    def __init__(self, *args):
        self._name = ""
        if len(args) == 0:
            self._width = 5
            self._height = 5
            self._matrix = [[0 for k in range(self._width)] for i in range(self._height)]

        if len(args) == 1 and type(args[0]) == str:
            s = args[0]
            if s[-1] == ":" or s[-1] == "\n":
                s = s[:-1]
            li = s.split(':')
            if len(li) == 1:
                li = args[0].split('\n')
            if len(li) > 1:
                self._height = len(li)
                self._width = len(li[0])
                self._matrix = [[0 for k in range(self._width)] for i in range(self._height)]
                for i in range(self._height):
                    for k in range(self._width):
                        self._matrix[i][k] = int(li[i][k])

        if len(args) == 2: 
            if type(args[1]) == str:  # for internal use
                self._name = args[1]
                self._height = 5
                self._width = 5
                self._matrix = [[0 for k in range(self._width)] for i in range(self._height)]
                for i in range(5):
                    for k in range(5):
                        self._matrix[i][k] = (9 if args[0][5 * i + k] == 1 else 0)
            else:
                self._width = args[0]
                self._height = args[1]
                self._matrix = [[0 for k in range(self._width)] for i in range(self._height)]
                    
        if len(args) == 3:
            self._width = args[0]
            self._height = args[1]
            self._matrix = args[2]

    def getMatrix(self):
        return self._matrix
 
    def setMatrix(self, matrix):
        self._matrix = matrix[:]

    def getName(self):
        return self._name

    def __str__(self):
        s = "Image(\n    '"
        for i in range(self._height):
            for k in range(self._width):
                s += str(self._matrix[i][k])
            if i < self._height - 1:    
                s += ":'\n    '" 
            else:   
                s += ":'\n" 
        s += ")"    
        return s
    
    def width(self):
        """Return the number of columns in the image."""
        return self._width

    def height(self):
        """Return the numbers of rows in the image."""
        return self._height
                
    def set_pixel(self, x, y, value):
        """Set the brightness of the pixel at column x and row y to the value, which has to be between 0 (dark) and 9 (bright)."""
        self._matrix[y][x] = value
        
    def get_pixel(self, x, y):    
        """Return the brightness of pixel at column x and row y as an integer between 0 and 9."""
        return self._matrix[y][x]
    
    def _shiftLeft(self, li, n):
        n = min(n, len(li))
        return li[n:] + [0] * n

    def _shiftRight(self, li, n):
        n = min(n, len(li))
        return [0] * n + li[:-n]

    def shift_left(self, n):
        """Return a new image created by shifting the picture left by n columns."""
        if n < 0:
            self.shift_right(-n)
        tmp = []
        for i in range(self._height):
            tmp.append(self._shiftLeft(self._matrix[i], n))
        return Image(self._width, self._height, tmp)
                    
    def shift_right(self, n):
        """Return a new image created by shifting the picture right by n columns."""
        if n < 0:
            self.shift_left(-n)
        tmp = []
        for i in range(self._height):
            tmp.append(self._shiftRight(self._matrix[i], n))
        return Image(self._width, self._height, tmp)
                    
    def shift_down(self, n):
        """Return a new image created by shifting the picture down by n rows."""
        if n < 0:
            self.shift_up(-n)
        n = min(n, self._height)
        tmp = [[0 for k in range(self._width)] for i in range(n)] + self._matrix[:-n]
        return Image(self._width, self._height, tmp)
                    
    def shift_up(self, n):
        """Return a new image created by shifting the picture up by n rows."""
        if n < 0:
            self.shift_down(-n)
        n = min(n, self._height)
        tmp = self._matrix[n:] + [[0 for k in range(self._width)] for i in range(n)]
        return Image(self._width, self._height, tmp)

    def crop(self, x, y, w, h):
        """Return a new image by cropping the picture to a width of w and a height of h, starting with the pixel at column x and row y."""
        tmp = [[0 for k in range(w)] for i in range(h)]
        for i in range(y, y + h):
            for k in range(x, x + w):
                if i < self._height and k < self._width:
                    tmp[i - y][k - x] = self._matrix[i][k]
        return Image(w, h, tmp)
    
    def copy(self):
        """Return an exact copy of the image."""
        img = Image(self._width, self._height, self._matrix)
        img._name = self._name
        return img
    
    def invert(self):
        """Return a new image by inverting the brightness of the pixels in the source image."""
        img = self.copy()
        img._name = ""
        for i in range(self._height):
            for k in range(self._width):
                img._matrix[i][k] = 9 - self._matrix[i][k]
        return img
    
    def fill(self, value):
        """Set the brightness of all the pixels in the image to the value, which has to be between 0 (dark) and 9 (bright)."""
        self._name = ""
        for i in range(self._height):
            for k in range(self._width):
                self._matrix[i][k] = value

    def blit(self, src, x, y, w, h, xdest = 0, ydest = 0):
        """Copy the rectangle defined by x, y, w, h from the image src into this image at xdest, ydest. Areas in the source rectangle, but outside the source image are treated as having a value of 0."""
        img = src.crop(x, y, w, h)
        for i in range(img._height):
            for k in range(img._width):
                idest = i + ydest
                kdest = k + xdest
                if idest < self._height and kdest < self._width:
                    self._matrix[idest][kdest] = img._matrix[i][k]

    def __add__(self, other):
        img = self.copy()
        img._name = ""
        for i in range(self._height):
            for k in range(self._width):
                v = min(img._matrix[i][k] + other._matrix[i][k], 9)
                img._matrix[i][k] = v
        return img
            
    def __sub__(self, other):
        img = self.copy()
        img._name = ""
        for i in range(self._height):
            for k in range(self._width):
                v = max(img._matrix[i][k] - other._matrix[i][k], 0)
                img._matrix[i][k] = v
        return img

    def __mul__(self, n):
        img = self.copy()
        img._name = ""
        for i in range(self._width):
            for k in range(self._height):
                v = max(min(int(img._matrix[i][k] * n + 0.5), 9), 0)
                img._matrix[i][k] = v
        return img
                    

Image.HEART = Image(_HEART, "HEART")
Image.SMILE = Image(_SMILE, "SMILE")
Image.HEART_SMALL = Image(_HEART_SMALL, "HEART_SMALL")
Image.HAPPY = Image(_HAPPY, "HAPPY")
Image.SAD = Image(_SAD, "SAD")
Image.CONFUSED = Image(_CONFUSED, "CONFUSED")
Image.ANGRY = Image(_ANGRY, "ANGRY")
Image.ASLEEP = Image(_ASLEEP, "ASLEEP")
Image.SURPRISED = Image(_SURPRISED, "SURPRISED")
Image.SILLY = Image(_SILLY, "SILLY")
Image.FABULOUS = Image(_FABULOUS, "FABULOUS")
Image.MEH = Image(_MEH, "MEH")
Image.YES = Image(_YES, "YES")
Image.NO = Image(_NO, "NO")
Image.CLOCK12 = Image(_CLOCK12, "CLOCK12")
Image.CLOCK1 = Image(_CLOCK1, "CLOCK1")
Image.CLOCK2 = Image(_CLOCK2, "CLOCK2")
Image.CLOCK3 = Image(_CLOCK3, "CLOCK3")
Image.CLOCK4 = Image(_CLOCK4, "CLOCK4")
Image.CLOCK5 = Image(_CLOCK5, "CLOCK5")
Image.CLOCK6 = Image(_CLOCK6, "CLOCK6")
Image.CLOCK7 = Image(_CLOCK7, "CLOCK7")
Image.CLOCK8 = Image(_CLOCK8, "CLOCK8")
Image.CLOCK9 = Image(_CLOCK9, "CLOCK9")
Image.CLOCK10 = Image(_CLOCK10, "CLOCK10")
Image.CLOCK11 = Image(_CLOCK11, "CLOCK11")
Image.ARROW_N = Image(_ARROW_N, "ARROW_N")
Image.ARROW_NE = Image(_ARROW_NE, "ARROW_NE")
Image.ARROW_E = Image(_ARROW_E, "ARROW_E")
Image.ARROW_SE = Image(_ARROW_SE, "ARROW_SE")
Image.ARROW_S = Image(_ARROW_S, "ARROW_S")
Image.ARROW_SW = Image(_ARROW_SW, "ARROW_SW")
Image.ARROW_W = Image(_ARROW_W, "ARROW_W")
Image.ARROW_NW = Image(_ARROW_NW, "ARROW_NW")
Image.TRIANGLE = Image(_TRIANGLE, "TRIANGLE")
Image.TRIANGLE_LEFT = Image(_TRIANGLE_LEFT, "TRIANGLE_LEFT")
Image.CHESSBOARD = Image(_CHESSBOARD, "CHESSBOARD")
Image.DIAMOND = Image(_DIAMOND, "DIAMOND")
Image.DIAMOND_SMALL = Image(_DIAMOND_SMALL, "DIAMOND_SMALL")
Image.SQUARE = Image(_SQUARE, "SQUARE")
Image.SQUARE_SMALL = Image(_SQUARE_SMALL, "SQUARE_SMALL")
Image.RABBIT = Image(_RABBIT, "RABBIT")
Image.COW = Image(_COW, "COW")
Image.MUSIC_CROTCHET = Image(_MUSIC_CROTCHET, "MUSIC_CROTCHET")
Image.MUSIC_QUAVER = Image(_MUSIC_QUAVER, "MUSIC_QUAVER")
Image.MUSIC_QUAVERS = Image(_MUSIC_QUAVERS, "MUSIC_QUAVERS")
Image.PITCHFORK = Image(_PITCHFORK, "PITCHFORK")
Image.XMAS = Image(_XMAS, "XMAS")
Image.PACMAN = Image(_PACMAN, "PACMAN")
Image.TARGET = Image(_TARGET, "TARGET")
Image.TSHIRT = Image(_TSHIRT, "TSHIRT")
Image.ROLLERSKATE = Image(_ROLLERSKATE, "ROLLERSKATE")
Image.DUCK = Image(_DUCK, "DUCK")
Image.HOUSE = Image(_HOUSE, "HOUSE")
Image.TORTOISE = Image(_TORTOISE, "TORTOISE")
Image.BUTTERFLY = Image(_BUTTERFLY, "BUTTERFLY")
Image.STICKFIGURE = Image(_STICKFIGURE, "STICKFIGURE")
Image.GHOST = Image(_GHOST, "GHOST")
Image.SWORD = Image(_SWORD, "SWORD")
Image.GIRAFFE = Image(_GIRAFFE, "GIRAFFE")
Image.SKULL = Image(_SKULL, "SKULL")
Image.UMBRELLA = Image(_UMBRELLA, "UMBRELLA")
Image.SNAKE = Image(_SNAKE, "SNAKE")

Image.ALL = [
Image.HEART, Image.SMILE, Image.HEART_SMALL, Image.HAPPY, Image.SAD, Image.CONFUSED, Image.ANGRY, Image.ASLEEP,
Image.SURPRISED, Image.SILLY, Image.FABULOUS, Image.MEH, Image.YES, Image.NO, Image.CLOCK12, Image.CLOCK1,
Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, Image.CLOCK7, Image.CLOCK8,Image.CLOCK9,
Image.CLOCK10, Image.CLOCK11, Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE, Image.ARROW_S,
Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW, Image.TRIANGLE, Image.TRIANGLE_LEFT, Image.CHESSBOARD, Image.DIAMOND,
Image.DIAMOND_SMALL, Image.SQUARE, Image.SQUARE_SMALL, Image.RABBIT, Image.COW, Image.MUSIC_CROTCHET, Image.MUSIC_QUAVER,
Image.MUSIC_QUAVERS, Image.PITCHFORK, Image.XMAS, Image.PACMAN, Image.TARGET, Image.TSHIRT, Image.ROLLERSKATE,
Image.DUCK, Image.HOUSE, Image.TORTOISE, Image.BUTTERFLY, Image.STICKFIGURE, Image.GHOST, Image.SWORD, Image.GIRAFFE,
Image.SKULL, Image.UMBRELLA, Image.SNAKE]

Image.ALL_ARROWS = [
Image.ARROW_N, Image.ARROW_NE, Image.ARROW_E, Image.ARROW_SE, Image.ARROW_S,
Image.ARROW_SW, Image.ARROW_W, Image.ARROW_NW]

Image.ALL_CLOCKS = [
Image.CLOCK12, Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, 
Image.CLOCK7, Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11]
