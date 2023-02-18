#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.led import Leds

rotPercm = 1
cm = 1

tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
tank_drive.on_for_rotations(SpeedPercent(75), SpeedPercent(75), rotPercm*cm)
