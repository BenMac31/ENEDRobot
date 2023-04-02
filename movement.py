#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor
from ev3dev2.sound import Sound
import math


def move(inch, tank : MoveTank, power = 50):
    """Moves 'inch' inch forward (backwards is negative.)"""
    inch *= 0.4313007

    tank.on_for_rotations(
            SpeedPercent(power), SpeedPercent(power), inch
            )

def carefuleMove(inch, tank : MoveTank, us : UltrasonicSensor, sound : Sound, power = 50, carefulness = 15):
    """Moves 'inch' inch forward (backwards is negative.)"""
    inchEachTime=inch/int(inch/10);
    for i in range(int(inch/10)):
        distance = us.distance_centimeters_ping
        if distance > carefulness:
            move(inchEachTime, tank, power)
        else:
            sound.speak("Detected object {distance} inch away, refusing to move.");
            distance = us.distance_centimeters_ping
            while distance < carefulness:
                sleep(1);
                distance = us.distance_centimeters_ping


def turn(degrees, tank : MoveTank, power = 50):
    """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""
    tank.turn_degrees(
        speed=SpeedPercent(-power),
        target_angle=degrees,
    )


def fix_angle(gs : GyroSensor, degrees, tank : MoveTank, power = 50):
    """Puts the angle of the robot to be the angle provided, not sure if it is actually differant than 'turn' """
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=-(degrees-gs.angle)/2,
    )

def cartesian_move(x, y, tank : MoveTank, pos, power = 50):
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

# def vector_move(x, y, tank : MoveTank, pos, power = 50):
#     """Moves to an x and y location by first turning x nuber of degrees than moving x number of meters"""
#     turn((math.atan(y/x)*180)/math.pi, tank, power) # POSSIBLE ERROR LOCATED HERE. If an error occurs switch (y/x) to (x/y)
#     move(math.sqrt(x**2+y**2), tank, power)
#     pos[0]+=x
#     pos[1]+=y


def SubTask1A(inch, laps, tank : MoveTank, gs : GyroSensor, power = 50):
    dir = True
    for i in range(laps*2):
        move(dir*(inch*2)-inch, tank, power)
        # fix_angle(gs, 0, power/10, tank)
        dir = not dir


def SubTask1B(inch, laps, tank : MoveTank, gs : GyroSensor, sound, power = 50):
    dir = True
    for i in range(laps):
        move(inch, tank, power)
        turn((dir*360)-180, tank, power)
        # sound.speak(gs.angle_and_rate)
        dir = not dir
