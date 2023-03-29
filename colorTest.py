#!/usr/bin/env python3

from time import sleep
import display

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from ev3dev2.sensor import INPUT_1, INPUT_2


ts = TouchSensor(INPUT_1)
cs = ColorSensor(INPUT_2)

count = 0
barVal = 0
while count < 4:
    if ts.is_pressed:
        count += 1
        colVal = cs.value()
        if colVal > 50:
            barVal += 1*(2**count);
        sleep (0.5)
    # don't let this loop use 100% CPU
    sleep(0.01)

display.displayBarCode(barVal);
sleep(10);
