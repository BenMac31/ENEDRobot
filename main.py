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
gs = GyroSensor(INPUT_1)
ts = TouchSensor(INPUT_2)

# Calibrate gyroscope
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)
tank.gyro = gs

# Subtask 1A
# movement.SubTask1A(30, 10, tank, gs) # Produces error of 4.4.166667cm x, 2.666667cm y

# Subtask 1B
moveAmount=12*2.54
while True:
    if ts.is_pressed:
        movement.move(moveAmount, tank)
        sleep (1)
    # don't let this loop use 100% CPU
    sleep(0.01)
