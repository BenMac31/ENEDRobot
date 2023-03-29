#!/usr/bin/env python3

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1


def displayBarCode(number):
    for binary in '{0:04b}'.format(number):
        if binary == "1":
            print("#", end='')
        else:
            print(" ", end='')
    print()

displayBarCode(5);
