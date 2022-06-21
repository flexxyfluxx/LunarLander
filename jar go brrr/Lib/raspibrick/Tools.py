# Tools.py
# Remote mode

import time
import SharedConstants

class Tools():
    def __init__(self):
        self.startTime = 0

    def startTimer(self):
        self.startTime = time.clock()

    def getTime(self):
        if self.startTime == 0:
            return 0
        else:
            return int(1000 * (time.clock() - self.startTime))

    @staticmethod
    def debug(text):
        if SharedConstants.DEBUG:
            print text

    @staticmethod
    def delay(interval):
        """
        Suspends execution for a given time inverval.
        @param interval: the time interval in milliseconds (ms)
        @return: none
        """
        time.sleep(interval / 1000.0)


