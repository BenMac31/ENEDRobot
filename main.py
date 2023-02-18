#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

rotPercm = 1
cm = 1

A = LargeMotor(OUTPUT_A)
A.on_for_rotations(SpeedPercent(75), rotPercm*cm)
B = LargeMotor(OUTPUT_B)
B.on_for_rotations(SpeedPercent(75), rotPercm*cm)
