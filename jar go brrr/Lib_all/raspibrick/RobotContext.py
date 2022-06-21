# RobotContext.py

from raspibrick.Obstacle import Obstacle
from raspibrick.Target import Target
from raspibrick.Torch import Torch

class RobotContext():
    '''
    Dummy class to make RaspiBrick source compatible with RaspiSim. All methods are empty.
    '''

    box = Obstacle("sprites/box.gif")
    channel = Obstacle("sprites/channel.gif")

    def __init__(self):
        pass

    @staticmethod
    def addMouseListener(listener):
        pass

    @staticmethod
    def init():
        pass

    @staticmethod
    def useBackground(filename):
        pass

    @staticmethod
    def setStartPosition(x, y):
        pass

    @staticmethod
    def setStartDirection(direction):
        pass

    @staticmethod
    def setLocation(x, y):
        pass

    @staticmethod
    def useObstacle(*args):
        pass

    @staticmethod
    def useTarget(*args):
        pass

    @staticmethod
    def useTorch(*args):
        pass

    @staticmethod
    def useShadow(*args):
        pass

    @staticmethod
    def showNavigationBar(*args):
        pass

    @staticmethod
    def showStatusBar(height):
        pass

    @staticmethod
    def setStatusText(text):
        pass
