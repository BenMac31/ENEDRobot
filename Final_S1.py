#!/usr/bin/env python3

import ROBOT

robot = ROBOT.Robot(["move", "gyro", "us"])

robot.move(36)
robot.turn(90)
robot.move(26)
robot.move(10)
robot.turn(90)
robot.move(36)
robot.move_to_home("B", atHome=False)
