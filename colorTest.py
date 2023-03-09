#!/usr/bin/env python3

from time import sleep

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor, TouchSensor
from ev3dev2.sensor import INPUT_1, INPUT_2


ts = TouchSensor(INPUT_1)
cs = ColorSensor(INPUT_2)

while True:
    if ts.is_pressed:
        print(cs.value())
        sleep (1)
    # don't let this loop use 100% CPU
    sleep(0.01)
