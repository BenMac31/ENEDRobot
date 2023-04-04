#!/usr/bin/env python3

from time import sleep
import threading

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
from ev3dev2.wheel import EV3EducationSetRim


tank = MoveTank(OUTPUT_A, OUTPUT_D)
test = LargeMotor(OUTPUT_A)
sound = Sound()
us = UltrasonicSensor(INPUT_2)
stopOnDetect = True
distance = 999

def stopIfDistance():
    while True:
        distance = us.distance_inches
        if stopOnDetect and distance[0] < 12:
            tank.off()
            sound.speak("Obstacle detected at " + str(distance) + " inches. Exiting program.")
            quit()

def readPositions():
    while True:
        pos = test.rotations
        sound.speak(str((pos)/0.4313007) + "In")

inch = 120

"""Moves 'inch' inch forward (backwards is negative.)"""
threading.Thread(target=stopIfDistance, args=(), daemon=True).start()
threading.Thread(target=readPositions, args=(), daemon=True).start()
tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 12*0.4313007)
tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 24*0.4313007)
tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 36*0.4313007)
tank.on_for_rotations(SpeedPercent(50), SpeedPercent(50), 48*0.4313007)
