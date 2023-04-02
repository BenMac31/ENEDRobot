#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math
import movement
from ev3dev2.wheel import EV3EducationSetRim


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
us = UltrasonicSensor(INPUT_2)

# Subtask 1A
# movement.SubTask1A(30, 10, tank, gs) # Produces error of 4.4.166667cm x, 2.666667cm y

sound.speak("Testing careful movement, robot will move 10 ft forward and stop if there is an obstacle.")
movement.careful_move(120, tank, us, sound)
