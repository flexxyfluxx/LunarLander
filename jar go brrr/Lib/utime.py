# utime.py
# Version 1.00 - April 26, 2019

import time

# code from utime source (not used)
MP_SMALL_INT_POSITIVE_MASK = ~(0xffff800000000000 | (0xffff800000000000 >> 1))  
MICROPY_PY_UTIME_TICKS_PERIOD = MP_SMALL_INT_POSITIVE_MASK + 1

def sleep(seconds):
    '''
    Sleep for the given number of seconds. You can use a floating-point number to sleep 
    for a fractional number of seconds, or use the utime.sleep_ms() and utime.sleep_us() functions.
    '''
    time.sleep(seconds)

def sleep_ms(ms):
    '''
    Delay for given number of milliseconds, should be positive or 0.
    '''
    time.sleep(ms / 1000)

def sleep_us(us):
    '''
    Delay for given number of microseconds, should be positive or 0.
    '''
    time.sleep(us / 1000000)

def ticks_ms():
    '''
    Returns an increasing millisecond counter with an arbitrary reference point. 
    (no wrap around link in MicroPython) 
    '''
#    return int(time.time() * 1000) & (MICROPY_PY_UTIME_TICKS_PERIOD - 1)
    return int(time.clock() * 1000)

def ticks_us():
    '''
    Just like utime.ticks_ms() above, but in microseconds.
    '''
#    return int(time.time() * 1000000) & (MICROPY_PY_UTIME_TICKS_PERIOD - 1)
    return int(time.time() * 1000000)

def ticks_add(ticks, delta):
    '''
    Offset ticks value by a given number, which can be either positive or negative. 
    '''
    return ticks_us() + delta

def ticks_diff(ticks1, ticks2):
    '''
    Measure ticks difference between values returned from utime.ticks_ms() or ticks_us() functions 
    '''
    return ticks1 - ticks2

ticks_cpu = ticks_us
            