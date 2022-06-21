# This is a mock-module to support auto-completion. The actual 
# module is located on the firmware of the micro:bit.
#
# Version: August-16-2017
#
# This file is part of TigerJython (www.tigerjython.ch)
#
# Source: https://microbit-micropython.readthedocs.io/en/latest/microbit.html

# Functions

def panic(n):
    """Enter a panic mode. Requires restart. Pass in an arbitrary integer <= 255 to indicate a status."""
    raise NotImplementedError("Execute your program on the micro:bit.")

def reset():
    """Restart the board."""
    raise NotImplementedError("Execute your program on the micro:bit.")

def sleep(n):
    """Wait for n milliseconds. One second is 1000 milliseconds."""
    raise NotImplementedError("Execute your program on the micro:bit.")

def running_time():
    """Return the number of milliseconds since the board was switched on or restarted."""
    raise NotImplementedError("Execute your program on the micro:bit.")

def temperature():
    """Return the temperature of the micro:bit in degrees Celcius."""
    raise NotImplementedError("Execute your program on the micro:bit.")

# Attributes

class Button():
    
    def is_pressed(self):
        """Returns True if the specified button button is pressed, and False otherwise."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def was_pressed(self):
        """Returns True or False to indicate if the button was pressed since the device started or the last time this method was called."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_presses(self):
        """Returns the running total of button presses, and resets this total to zero before returning."""
        raise NotImplementedError("Execute your program on the micro:bit.")

button_a = Button()
button_b = Button()

class MicroBitDigitalPin():

    def read_digital(self):
        """Return 1 if the pin is high, and 0 if it is low."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def write_digital(self, value):
        """Set the pin to high if value is 1, or to low, if it is 0."""
        raise NotImplementedError("Execute your program on the micro:bit.")

class MicroBitAnalogDigitalPin():
    
    def read_analog(self):
        """Read the voltage applied to the pin, and return it as an integer between 0 (meaning 0V) and 1023 (meaning 3.3V)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def write_analog(self, value):
        """Output a PWM signal on the pin, with the duty cycle proportional to the provided value. The value may be either an integer or a floating point number between 0 (0% duty cycle) and 1023 (100% duty)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def set_analog_period(self, period):
        """Set the period of the PWM signal being output to period in milliseconds. The minimum valid value is 1ms."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def set_analog_period_microseconds(self, period):
        """Set the period of the PWM signal being output to period in microseconds. The minimum valid value is 256s."""
        raise NotImplementedError("Execute your program on the micro:bit.")

class MicroBitTouchPin():

    def is_touched(self):
        """Return True if the pin is being touched with a finger, otherwise return False."""
        raise NotImplementedError("Execute your program on the micro:bit.")
    
# Image class

class Image():
    def __init__(self, *args, **kwargs):
        pass

    def width(self):
        """Return the number of columns in the image."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def height(self):
        """Return the numbers of rows in the image."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def set_pixel(self, x, y, value):
        """Set the brightness of the pixel at column x and row y to the value, which has to be between 0 (dark) and 9 (bright)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_pixel(self, x, y):
        """Return the brightness of pixel at column x and row y as an integer between 0 and 9."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def shift_left(self, n):
        """Return a new image created by shifting the picture left by n columns."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def shift_right(self, n):
        """Same as image.shift_left(-n)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def shift_up(self, n):
        """Return a new image created by shifting the picture up by n rows."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def shift_down(self, n):
        """Same as image.shift_up(-n)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def crop(self, x, y, w, h):
        """Return a new image by cropping the picture to a width of w and a height of h, starting with the pixel at column x and row y."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def copy(self):
        """Return an exact copy of the image."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def invert(self):
        """Return a new image by inverting the brightness of the pixels in the source image."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def fill(self, value):
        """Set the brightness of all the pixels in the image to the value, which has to be between 0 (dark) and 9 (bright)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def blit(self, src, x, y, w, h, xdest=0, ydest=0):
        """Copy the rectangle defined by x, y, w, h from the image src into this image at xdest, ydest. Areas in the source rectangle, but outside the source image are treated as having a value of 0."""
        raise NotImplementedError("Execute your program on the micro:bit.")

Image.HEART = Image()
Image.HEART_SMALL = Image()
Image.HAPPY = Image()
Image.SMILE = Image()
Image.SAD = Image()
Image.CONFUSED = Image()
Image.ANGRY = Image()
Image.ASLEEP = Image()
Image.SURPRISED = Image()
Image.SILLY = Image()
Image.FABULOUS = Image()
Image.MEH = Image()
Image.YES = Image()
Image.NO = Image()
Image.CLOCK12 = Image()
Image.CLOCK11 = Image()
Image.CLOCK10 = Image()
Image.CLOCK9 = Image()
Image.CLOCK8 = Image()
Image.CLOCK7 = Image()
Image.CLOCK6 = Image()
Image.CLOCK5 = Image()
Image.CLOCK4 = Image()
Image.CLOCK3 = Image()
Image.CLOCK2 = Image()
Image.CLOCK1 = Image()
Image.ARROW_N = Image()
Image.ARROW_NE = Image()
Image.ARROW_E = Image()
Image.ARROW_SE = Image()
Image.ARROW_S = Image()
Image.ARROW_SW = Image()
Image.ARROW_W = Image()
Image.ARROW_NW = Image()
Image.TRIANGLE = Image()
Image.TRIANGLE_LEFT = Image()
Image.CHESSBOARD = Image()
Image.DIAMOND = Image()
Image.DIAMOND_SMALL = Image()
Image.SQUARE = Image()
Image.SQUARE_SMALL = Image()
Image.RABBIT = Image()
Image.COW = Image()
Image.MUSIC_CROTCHET = Image()
Image.MUSIC_QUAVER = Image()
Image.MUSIC_QUAVERS = Image()
Image.PITCHFORK = Image()
Image.XMAS = Image()
Image.PACMAN = Image()
Image.TARGET = Image()
Image.TSHIRT = Image()
Image.ROLLERSKATE = Image()
Image.DUCK = Image()
Image.HOUSE = Image()
Image.TORTOISE = Image()
Image.BUTTERFLY = Image()
Image.STICKFIGURE = Image()
Image.GHOST = Image()
Image.SWORD = Image()
Image.GIRAFFE = Image()
Image.SKULL = Image()
Image.UMBRELLA = Image()
Image.SNAKE = Image()

# Display-module

class _Display():

    def get_pixel(self, x, y):
        """Return the brightness of the LED at column x and row y as an integer between 0 (off) and 9 (bright)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def set_pixel(self, x, y, value):
        """Set the brightness of the LED at column x and row y to value, which has to be an integer between 0 and 9."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def clear(self):
        """Set the brightness of all LEDs to 0 (off)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def show(self, image, delay=400, wait=True, loop=False, clear=False):
        """Display images or letters from the iterable in sequence, with delay milliseconds between them."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def scroll(self, string, delay=150, wait=True, loop=False, monospace=False):
        """Similar to show, but scrolls the string horizontally instead. The delay parameter controls how fast the text is scrolling."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def on(self):
        """Use on() to turn on the display."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def off(self):
        """Use off() to turn off the display (thus allowing you to re-use the GPIO pins associated with the display for other purposes)."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def is_on(self):
        """Returns True if the display is on, otherwise returns False."""
        raise NotImplementedError("Execute your program on the micro:bit.")
        
display = _Display()
        
# Accelerometer-module

class _Accelerometer():

    def get_x(self):
        """Get the acceleration measurement in the x axis, as a positive or negative integer, depending on the direction."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_y(self):
        """Get the acceleration measurement in the y axis, as a positive or negative integer, depending on the direction."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_z(self):
        """Get the acceleration measurement in the z axis, as a positive or negative integer, depending on the direction."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_values(self):
        """Get the acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def current_gesture(self):
        """Return the name of the current gesture."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def is_gesture(self, name):
        """Return True or False to indicate if the named gesture is currently active."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def was_gesture(self, name):
        """Return True or False to indicate if the named gesture was active since the last call."""
        raise NotImplementedError("Execute your program on the micro:bit.")

    def get_gestures(self):
        """Return a tuple of the gesture history. The most recent is listed last. Also clears the gesture history before returning."""
        raise NotImplementedError("Execute your program on the micro:bit.")

accelerometer = _Accelerometer()

print "TigerJython cannot run your micro:bit-program.\nPlease download your program to your micro:bit."
raise NotImplementedError("TigerJython cannot run your micro:bit-program.\nPlease download your program to your micro:bit.")
