#!/usr/bin/env python3

import ROBOT

robot = ROBOT.Robot(["move", "gyro", "us"])

robot.home = "B"
robot.move_to_home("A")
