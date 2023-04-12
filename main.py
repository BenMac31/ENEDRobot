#!/usr/bin/env python3

import ROBOT

robot = ROBOT.Robot(["move", "gyro", "us"])

robot.move_to_loc(["A1", 9])
