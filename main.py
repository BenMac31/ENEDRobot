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
us = UltrasonicSensor(INPUT_2)

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
pos=[0,0]
movement.cartesian_move(50, 50, tank, pos)
sound.speak("Please move robot back to original position.")
sound.speak("Robot should move to the same position it previously moved to, if it does not please alert lead programmer.")
sleep(10)
movement.vector_move(50, 50, tank, pos)
sound.speak("Current position should be 100, 100")
sound.speak(f"current position is: {pos[0]}, {pos[1]}")
sound.speak("If these positions differ please alert lead programmer.")
sound.speak("Should return to original position if it does not, please alart lead programmer.")
movement.vector_move(-50, -50, tank, pos)
sound.speak("Current position should be 50, 50")
sound.speak(f"current position is: {pos[0]}, {pos[1]}")
sound.speak("If these positions differ please alert lead programmer.")
sound.speak("Testing careful movement, robot will move 1 meter forward and stop if there is an obstacle.")
movement.carefuleMove(100, tank, us, sound)
