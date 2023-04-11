#!/usr/bin/env python3

import ROBOT

robot = ROBOT.Robot(["move", "gyro"]);

angle = input("Angle: ")
while angle != "Q":
    robot.turn(int(angle))
    print(str(robot.gy.value()))
    angle = input("Angle: ")
