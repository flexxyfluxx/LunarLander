# nxtrobot.py
# AP
# Version 1.07, Nov 8, 2017

import os
from enum import enum

def loadLib(libfile):
   jarFile = getTigerJythonPath("Lib") + libfile
   if not os.path.exists(jarFile):
      raise IOError("Cannot find '" + libfile + "' - Please copy it in <tigerjython_home>/Lib.")
   from java.net import URL, URLClassLoader
   from java.lang import ClassLoader
   from java.io import File
   m = URLClassLoader.getDeclaredMethod("addURL", [URL])
   m.accessible = 1
   m.invoke(ClassLoader.getSystemClassLoader(), [File(jarFile).toURL()])



#loadLib("bluecove-2.1.1-SNAPSHOT.jar")
#loadLib("bluecove-gpl-2.1.1-SNAPSHOT.jar")
from ch.aplu.nxt import *
from javax.swing import *
from java.awt import *
