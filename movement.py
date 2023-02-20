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


def fix_angle(gs, degrees, power, tank):
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=(degrees-gs.angle)/2,
    )


def SubTask1A(cm, laps, tank, gs, power=30):
    dir = True
    for i in range(laps*2):
        move(dir*(cm*2)-cm, power, tank)
        # fix_angle(gs, 0, power/10, tank)
        dir = not dir


def SubTask1B(cm, laps, tank, gs, sound, power=30):
    dir = True
    for i in range(laps):
        move(cm, power, tank)
        turn(dir*180, power, tank)
        sound.speak(gs.angle_and_rate)
        dir = not dir
