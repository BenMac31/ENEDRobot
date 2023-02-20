#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds
import math


def move(inches, power):
    rotPerInch = 0.1395546

    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(
            SpeedPercent(-power), SpeedPercent(-power), inches*rotPerInch
            )


def turn(degrees, power):
    rotPerDeg = 0.5582184

    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(
            SpeedPercent(-power), SpeedPercent(power), degrees*rotPerDeg
            )


# move(10, 50)
turn(math.pi, 50)
# move(10, 50)
