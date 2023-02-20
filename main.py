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


# tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
# gs = GyroSensor(INPUT_1)

# # Calibrate gyroscope
# sound.speak("Calibrating, do not touch mindstorm.")
# sleep(1)
# gs.calibrate()
# sound.speak("Calibration complete.")
# sleep(1)
# tank.gyro = gs

# Subtask 1A
# movement.SubTask1A(30, 10, tank)
# # Rotate 90 degrees clockwise

mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3EducationSetRim, 86)

sound.speak("Turn right 90")
mdiff.turn_right(SpeedRPM(40), 90)

# # Drive forward 500 mm
sound.speak("Drive forward 500 m m")
mdiff.on_for_distance(SpeedRPM(40), 500)

sound.speak("Drive in arc to the right along an imaginary circle of radius 150 m m.")
mdiff.on_arc_right(SpeedRPM(40), 150, 700)

# # Enable odometry
mdiff.odometry_start()

# # Use odometry to drive to specific coordinates
sound.speak("Go to 300, 300")
mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)

# # Use odometry to go back to where we started
sound.speak("Go to 0, 0")
mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

# # Use odometry to rotate in place to 90 degrees
sound.speak("Turn to angle 90")
mdiff.turn_to_angle(SpeedRPM(40), 90)

# # Disable odometry
# mdiff.odometry_stop()
