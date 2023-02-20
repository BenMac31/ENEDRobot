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
def turn(degrees, power):
    tank.turn_degrees(
        speed=SpeedPercent(power),
        target_angle=degrees,
    )


sound = Sound()

gs = GyroSensor(INPUT_1)

sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)

tank.gyro = gs
dir = True

for i in range(6):
    move(10, 30)
    turn((-1*dir)*180, 30)
    dir = not dir
