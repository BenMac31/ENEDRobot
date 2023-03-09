#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math
from ev3dev2.wheel import EV3EducationSetRim

import sensors


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
cs = ColorSensor(INPUT_3)

# Calibrate gyroscope
sensors.readBarcode(cs, tank)
sleep(10)
