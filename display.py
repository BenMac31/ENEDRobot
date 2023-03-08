#!/usr/bin/env python3

from time import sleep
import movement

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math


def displayBarCode(number):
    for binary in '{0:04b}'.format(number):
        if binary == "1":
            print("█", end='')
        else:
            print(" ", end='')
    print()

displayBarCode(5);
