#!/usr/bin/env python3

from time import sleep
import movement
import display

from ev3dev2.motor import LargeMotor, SpeedPercent, MoveTank
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.sound import Sound
import math
import random

def blackOrWhite(cs : ColorSensor):
    return (random.randint(0, 1))

def readBarcode(cs : ColorSensor, tank : MoveTank):
    value = 0
    for i in range(4):
        movement.move(1.27, tank);
        value += blackOrWhite(cs)*(2**i)
    display.displayBarCode(value);
