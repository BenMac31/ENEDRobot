#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math

def move(cm, power, tank):
    cm *= 0.05494276

    tank.on_for_rotations(
            SpeedPercent(-power), SpeedPercent(-power), cm
            )

def turn(degrees, power, tank):
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=degrees,
    )

def SubTask1A(cm, laps, tank, power=30):
    dir = True
    for i in range(laps*2):
        move(dir*(cm*2)-cm, power, tank)
        dir = not dir
