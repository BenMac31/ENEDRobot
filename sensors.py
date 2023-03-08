#!/usr/bin/env python3

from time import sleep
import movement

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor, ColorSensor, TouchSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math


ts = TouchSensor()
leds = Leds()

print("Press the touch sensor to change the LED color!")

while True:
    if ts.is_pressed:
        pass
    # don't let this loop use 100% CPU
    sleep(0.01)
