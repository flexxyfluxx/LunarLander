# enum.py
# AP
# Version 1.0, June 17, 2013

from java.lang import Enum

class JEnum(Enum):
   def __init__(self, s, i):
      Enum.__init__(self, s, i)

class enum():
   def __init__(self, *args):
      self.v = []
      i = 0
      for s in args:
         e = JEnum(s, i)
         params = {
            s: e,
            }
         self.__dict__.update(params)
         self.v.append(e)
         i += 1

   def values(self):
      return self.v
   
