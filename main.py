#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math


tank = MoveTank(OUTPUT_A, OUTPUT_D)


def move(inches, power):
    rotPerInch = 0.1395546

    tank.on_for_rotations(
            SpeedPercent(-power), SpeedPercent(-power), inches*rotPerInch
            )


sound = Sound()

gs = GyroSensor(INPUT_1)

sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)

tank.gyro = gs

# move(10, 50)
tank.turn_degrees(
    speed=SpeedPercent(30),
    target_angle=180,
)
