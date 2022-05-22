from __future__ import print_function
import math as m
from random import randint


for c in range(100):
    value = c
    value = 0 if value < 30 else value
    value = 100 if value > 70 else value
    value = (6 * value ** 5 - 15 * value ** 4 + 10 * value ** 3) % 100

    for z in range(value):
        print("#", end = "")
    print("")