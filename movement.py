#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math


def move(cm, power, tank):
    """Moves 'cm' cm forward (backwards is negative.)"""
    cm *= 0.05494276

    tank.on_for_rotations(
            SpeedPercent(-power), SpeedPercent(-power), cm
            )


def turn(degrees, power, tank):
    """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=degrees,
    )


def fix_angle(gs, degrees, power, tank):
    """Puts the angle of the robot to be the angle provided, not sure if it is actually differant than 'turn' """
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=(degrees-gs.angle)/2,
    )

def cartesian_move(x, y, power, tank, pos):
    """Moves to an x and y location by first moving to the y position, then turning 90 degrees and moving to the x location."""
    move(y, power, tank)
    turn(90, power, tank)
    move(x, power, tank)
    pos[0]+=x
    pos[1]+=y

def vector_move(x, y, power, tank, pos):
    """Moves to an x and y location by first turning x nuber of degrees than moving x number of meters"""
    turn((math.atan(y/x)*180)/math.pi, power, tank) # POSSIBLE ERROR LOCATED HERE. If an error occurs switch (y/x) to (x/y)
    move(math.sqrt(x**2+y**2), power, tank)
    pos[0]+=x
    pos[1]+=y


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
        turn((dir*360)-180, power, tank)
        # sound.speak(gs.angle_and_rate)
        dir = not dir
