#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, GyroSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math
import movement
from ev3dev2.wheel import EV3Tire


# tank = MoveTank(OUTPUT_A, OUTPUT_D)
# sound = Sound()
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
STUD_MM=8
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 8 * STUD_MM)
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 16 * STUD_MM)

# Rotate 90 degrees clockwise
mdiff.turn_right(SpeedRPM(40), 90)

# Drive forward 500 mm
mdiff.on_for_distance(SpeedRPM(40), 500)

# Drive in arc to the right along an imaginary circle of radius 150 mm.
# Drive for 700 mm around this imaginary circle.
mdiff.on_arc_right(SpeedRPM(80), 150, 700)

# Enable odometry
mdiff.odometry_start()

# Use odometry to drive to specific coordinates
mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)

# Use odometry to go back to where we started
mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

# Use odometry to rotate in place to 90 degrees
mdiff.turn_to_angle(SpeedRPM(40), 90)

# Disable odometry
mdiff.odometry_stop()
