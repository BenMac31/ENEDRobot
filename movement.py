#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor
from ev3dev2.sound import Sound
import math


def move(cm, tank : MoveTank, power = 10):
    """Moves 'cm' cm forward (backwards is negative.)"""
    cm *= 0.01766697

    tank.on_for_rotations(
            SpeedPercent(power), SpeedPercent(power), cm
            )

def carefuleMove(cm, tank : MoveTank, us : UltrasonicSensor, sound : Sound, power = 10, carefulness = 15):
    """Moves 'cm' cm forward (backwards is negative.)"""
    cmEachTime=cm/int(cm/10);
    for i in range(int(cm/10)):
        distance = us.distance_centimeters_ping
        if distance > carefulness:
            move(cmEachTime, tank, power)
        else:
            sound.speak("Detected object {distance} cm away, refusing to move.");
            distance = us.distance_centimeters_ping
            while distance < carefulness:
                sleep(1);
                distance = us.distance_centimeters_ping


def turn(degrees, tank : MoveTank, power = 10):
    """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""
    tank.turn_degrees(
        speed=SpeedPercent(-power),
        target_angle=degrees,
    )


def fix_angle(gs : GyroSensor, degrees, tank : MoveTank, power = 10):
    """Puts the angle of the robot to be the angle provided, not sure if it is actually differant than 'turn' """
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=-(degrees-gs.angle)/2,
    )

def cartesian_move(x, y, tank : MoveTank, pos, power = 10):
    """Moves to an x and y location by first moving to the y position, then turning 90 degrees and moving to the x location."""
    if y!=0:
        move(y, tank, power)
    if x!=0:
        turnDir=(x < 0)*-2+1
        turn(90*turnDir, tank, power)
        x=abs(x)
        move(x, tank, power)
        turn(90*turnDir, tank, power)
    pos[0]+=x
    pos[1]+=y

# def vector_move(x, y, tank : MoveTank, pos, power = 10):
#     """Moves to an x and y location by first turning x nuber of degrees than moving x number of meters"""
#     turn((math.atan(y/x)*180)/math.pi, tank, power) # POSSIBLE ERROR LOCATED HERE. If an error occurs switch (y/x) to (x/y)
#     move(math.sqrt(x**2+y**2), tank, power)
#     pos[0]+=x
#     pos[1]+=y


def SubTask1A(cm, laps, tank : MoveTank, gs : GyroSensor, power=10):
    dir = True
    for i in range(laps*2):
        move(dir*(cm*2)-cm, tank, power)
        # fix_angle(gs, 0, power/10, tank)
        dir = not dir


def SubTask1B(cm, laps, tank : MoveTank, gs : GyroSensor, sound, power=10):
    dir = True
    for i in range(laps):
        move(cm, tank, power)
        turn((dir*360)-180, tank, power)
        # sound.speak(gs.angle_and_rate)
        dir = not dir
