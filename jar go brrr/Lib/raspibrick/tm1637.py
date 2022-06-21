# tm1637.py
# Version 1.00

import RPi.GPIO as GPIO
from time import sleep

PATTERN = b'\0\x86\x22\0\0\0\0\x02\0\0\0\0\x04\x40\x80\x52\x3f\x06\x5b\x4f\x66\x6d\x7d\x07\x7f\x6f\0\0\0\x48\0\0\x5d\x77\x7c\x39\x5e\x79\x71\x3d\x76\x30\x0e\x70\x38\x55\x54\x3f\x73\x67\x50\x2d\x78\x3e\x36\x6a\x49\x6e\x1b\x39\x64\x0f\x23\x08\x20\x77\x7c\x58\x5e\x79\x71\x3d\x74\x10\x0c\x70\x30\x55\x54\x5c\x73\x67\x50\x2d\x78\x1c\x36\x6a\x49\x6e\x1b\0\x30\0\x41'

class FourDigit:
    myData = [0,0,0,0]
    
    def __init__(self, dio = 38, clk = 40, lum = 4):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.clk = clk
        self.dio = dio
        self.lum = lum
        self.colon = False
        self.startPos = 0
        self.text = None
        GPIO.setup(clk, GPIO.OUT)
        GPIO.setup(dio, GPIO.OUT)
        GPIO.output(clk, 0)
        GPIO.output(dio, 0)

    def erase(self):
        self.colon = False
        self.show("    ")

    def show(self, text, pos = 0):
        self.startPos = pos
        self.pos = pos
        self.text = str(text)  # digits to chars
        if len(self.text) < 4:
            self.text = "%-4s" % self.text
        self._cropText()
        
    def scroll(self, text):
        self.show(text)
        sleep(1.5)
        while self.toLeft() > 0:
            sleep(1)
        sleep(1)    
            
    def toRight(self):
        if self.text == None:
            return -1
        self.pos -= 1    
        self._cropText()
        return max(0, 4 + self.pos)

    def toLeft(self):
        if self.text == None:
            return -1
        self.pos += 1    
        self._cropText()
        nb = len(self.text) - self.pos
        return max(0, nb)

    def toStart(self):
        if self.text == None:
            return -1
        self.pos = self.startPos    
        self._cropText()
       
    def setLuminosity(self, lum):        
        self.lum = lum

    def setColon(self, enable):        
        self.colon = enable

    def _cropText(self):
        n = len(self.text)
        data = [' '] * (n + 8)
        for i in range(n):
            data[i + 4] = self.text[i]
        start = max(0, self.pos + 4)
        start = min(start, len(data) - 4)
        end = min(start + n, len(data))
        data = self._toSegment(data[start:end])
        self._prepare(0x40)    
        self._writeByte(0xC0)
        for i in range(4):
            self._writeByte(data[i])
        self._commit()
        
    def _writeByte(self, data):
        for i in range(8):
            GPIO.output(self.clk, 0)
            sleep(0.0001)
            if data & 0x01:
                GPIO.output(self.dio, 1)
            else:
                GPIO.output(self.dio, 0)
            sleep(0.0001)
            data = data >> 1
            GPIO.output(self.clk, 1)
            sleep(0.0001)

        GPIO.output(self.clk, 0)
        GPIO.output(self.dio, 1)
        GPIO.output(self.clk, 1)
        # wait for ACK, no need to set pin as input
        while GPIO.input(self.dio) == 1:
            sleep(0.001)
        sleep(0.001)
    
    def _toSegment(self, text):
        data = []
        msb = 0
        if self.colon:
            msb = 0x80
        for c in text:
            data.append(ord(PATTERN[ord(c) - 32]) + msb)
        return data

    def _start(self):
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)
        sleep(0.0001)
        GPIO.output(self.dio, 0) 
        GPIO.output(self.clk, 0) 
        sleep(0.0001)
    
    def _stop(self):
        GPIO.output(self.clk, 0) 
        GPIO.output(self.dio, 0) 
        sleep(0.0001)
        GPIO.output(self.clk, 1)
        GPIO.output(self.dio, 1)
        sleep(0.0001)
        
    def _prepare(self, addr):        
        self._start()
        self._writeByte(addr)
        self._stop()
        self._start()

    def _commit(self):
        self._stop()
        self._start()
        self._writeByte(0x88 + self.lum)
        self._stop()
