#!/usr/bin/env python3

import ROBOT

robot = ROBOT.Robot(["move", "gyro", "us"]);

robot.move(-12)
robot.move(12)
