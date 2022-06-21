# utils.py
# Simulation version
# Version 1.05 - June 12, 2018



# ------------------- Simple vector class --------------
class Vector:
    def __init__(self, *args):
        if len(args) == 2:
            self._vec = [args[0], args[1]]
        elif len(args) == 1:
            self._vec = list(args[0][:])
        else:
            self._vec = [0, 0]
            
    def add(self, otherVec):
        return Vector(self._vec[0] + otherVec[0], self._vec[1] + otherVec[1])

    def sub(self, otherVec):
        return Vector(self._vec[0] - otherVec[0], self._vec[1] - otherVec[1])

    def mult(self, k):
        return Vector(self._vec[0] * k, self._vec[1] * k)
        
    def __str__(self):
        return str(self._vec)    
    
    def __getitem__(self, index):
        return self._vec[index]

    def __setitem__(self, index, value):
         self._vec[index] = value
         
    def __eq__(self, other):
        return self._vec[0] == other._vec[0] and self._vec[1] == other._vec[1]
    
    def __ne__(self, other):
        return not self.__eq__(other)     
         
