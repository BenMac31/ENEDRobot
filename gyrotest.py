#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math

sound = Sound()

gs = GyroSensor(INPUT_1)
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
while True:
    print(gs.angle_and_rate)
    sleep(0.1)
