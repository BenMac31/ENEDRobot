#!/usr/bin/env python3

from time import sleep

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1

import display
import movement

tank = MoveTank(OUTPUT_A, OUTPUT_D)
cs = ColorSensor(INPUT_1)

count = 0
barVal = 0
while count < 4:
    movement.cartesian_move(0, 1.37*2.54, tank, [0, 0])
    count += 1
    colVal = cs.value()
    if colVal > 30:
        barVal += 1*(2**count);
    sleep(0.01)

display.displayBarCode(barVal);
sleep(10);
