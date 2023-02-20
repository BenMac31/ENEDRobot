#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math
import movement
from ev3dev2.wheel import EV3EducationSetRim


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
gs = GyroSensor(INPUT_1)

# Calibrate gyroscope
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)
tank.gyro = gs

# Subtask 1A
movement.SubTask1A(30, 10, tank, gs) # Produces error of 4.4.25cm x, 2.5cm y

# Subtask 1B
# movement.SubTask1B(30, 10, tank, gs, sound) # Produces error of 8cm y, 2.4x
