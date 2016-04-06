#!/usr/bin/python
import sys
import time
from sense_hat import SenseHat

X = (255, 204, 0)
O = (0, 51, 102)

question_mark = [
    X, O, O, O, O, O, X, X,
    X, O, O, O, O, O, X, O,
    O, X, O, X, O, X, O, O,
    O, O, X, O, X, O, O, O,
    O, O, O, O, O, O, X, X,
    O, O, O, X, O, X, O, O,
    O, O, O, O, X, O, O, O,
    O, O, O, O, O, O, O, O
]

sense = SenseHat()

sense.set_pixels(question_mark)
