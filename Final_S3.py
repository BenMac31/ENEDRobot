#!/usr/bin/env python3

import ROBOT
from time import sleep

robot = ROBOT.Robot(["move", "gyro", "us", "colour"])

# robot.move_to_loc(["A1", 9])
robot.move_to_unit(9)
robot.scan_barcode()
sleep(10)
