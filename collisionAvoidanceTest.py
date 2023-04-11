#!/usr/bin/env python3

from time import sleep
import threading

from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent, MoveTank, OUTPUT_D, FollowGyroAngleErrorTooFast, follow_for_ms
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor
from ev3dev2.sound import Sound


tank = MoveTank(OUTPUT_D, OUTPUT_A)
rm = LargeMotor(OUTPUT_A)
lm = LargeMotor(OUTPUT_D)
sound = Sound()
us = UltrasonicSensor(INPUT_2)
gs = GyroSensor(INPUT_1)
gs = GyroSensor(INPUT_1)

gs.calibrate()
tank.gyro = gs

distance = 999
pos = 0
usEnabled = True
usLock = False
posMod = 0

def followin(distance) -> bool:
    global usLock
    global posMod
    pos = ((rm.rotations+lm.rotations)/2) - posMod
    if pos > distance:
        print("Travelled " + str(int((pos)/0.4313007)) + " inches.")
        posMod += pos
        return False
    elif (usEnabled == True):
        obsDistance = us.distance_inches
        if (obsDistance < 12):
            print("Obstacle distance:" + str(int(obsDistance)) + " inches.")
            usLock = True
            posMod += pos
            return False
        else:
            return True
    else:
        return True

# threading.Thread(target=stopIfDistance, args=(), daemon=True).start()

while (not usLock):
    tank.follow_gyro_angle(
        kp=11.3, ki=0.05, kd=3.2,
        speed=SpeedPercent(50),
        target_angle=0,
        sleep_time=0.01,
        distance=240*0.4313007,
        follow_for=followin,
    )

print("Total distance:"+ str(int((rm.rotations+lm.rotations)/2/0.4313007)) + " inches.")
print("Angle:" + str(int(gs.angle)))
