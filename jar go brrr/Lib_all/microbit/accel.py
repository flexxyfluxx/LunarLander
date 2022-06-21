# accel.py
# Version 1.00 - July 2, 2018

from microbit import _sim
import time

class Accelerometer:
    _instance = None  
    
    def get_x(self):
        """Get the acceleration measurement in the x axis, as a positive or negative integer, depending on the direction."""
        Accelerometer._check()
        return 100 * _sim.getAccelX()

    def get_y(self):
        """Get the acceleration measurement in the y axis, as a positive or negative integer, depending on the direction."""
        Accelerometer._check()
        return 100 * _sim.getAccelY()

    def get_z(self):
        """Get the acceleration measurement in the z axis, as a positive or negative integer, depending on the direction."""
        Accelerometer._check()
        return 100 * _sim.getAccelZ()

    def get_values(self):
        """Get the acceleration measurements in all axes at once, as a three-element tuple of integers ordered as X, Y, Z."""
        Accelerometer._check()
        li = _sim.getAccelValues()[:]
        for i in range(3):
            li[i] = 100 * li[i]
        return tuple(li.tolist())

    def current_gesture(self):
        """Return the name of the current gesture."""
        Accelerometer._check()
        return _sim.getCurrentGesture()

    def is_gesture(self, name):
        """Return True or False to indicate if the named gesture is currently active."""
        Accelerometer._check()
        return _sim.getCurrentGesture() == name

    def was_gesture(self, name):
        """Return True or False to indicate if the named gesture was active since the last call."""
        Accelerometer._check()
        if name in self.get_gestures():
            return True
        return False

    def get_gestures(self):
        """Return a tuple of the gesture history. The most recent is listed last. Also clears the gesture history before returning."""
        Accelerometer._check()
        hist = _sim.getGestureHistory().tolist()
        _sim.clearGestureHistory()
        return tuple(hist)
    
    # ------------ private ---------------------
    @staticmethod
    def _check():
        if Accelerometer._instance == None:
            Accelerometer._instance = _sim.createAccelerometer()