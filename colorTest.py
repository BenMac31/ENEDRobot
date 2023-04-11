#!/usr/bin/env python3

from time import sleep

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.motor import OUTPUT_A, MoveTank, OUTPUT_D, OUTPUT_B, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_3

import display
import movement

tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
cs = ColorSensor(INPUT_3)
gs = GyroSensor(INPUT_1)
medMotor = MediumMotor(OUTPUT_B)

# Calibrate
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)
tank.gyro = gs

# Read values from barcode
barVal = 0
cols=[0 for i in range (4)]
for count in range(4):
    cols[count] = cs.value();
    sleep(0.1)
    movement.cartesian_move(0, 0.5, tank, [0, 0], 20)

# Calculate barcode number
colMin=max(cols)
for i in range(len(cols)):
    if cols[i] < colMin - 20:
        barVal += 1*(2**i)

# Display barcode
display.displayBarCode(barVal);

# Movement logic for picking up the box
movement.move(2, tank, 20)
movement.turn(90, tank, 20)
movement.move(1, tank, 20)
medMotor.on_for_rotations(-30, 4.5)
movement.move(-2, tank, 20)
medMotor.on_for_rotations(30, 4.5)
movement.move(12, tank, 20)
medMotor.on_for_rotations(-30, 4.5)
movement.move(6, tank, 50)
medMotor.on_for_rotations(30, 4.5)
