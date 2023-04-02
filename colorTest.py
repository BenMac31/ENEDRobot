#!/usr/bin/env python3

from time import sleep

# from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D
# from ev3dev2.sensor import INPUT_1
from ev3dev2.motor import OUTPUT_A, MoveTank, OUTPUT_D, OUTPUT_B, MediumMotor
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor
from ev3dev2.sensor import INPUT_1, INPUT_3

import display
import movement

tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
cs = ColorSensor(INPUT_3)
gs = GyroSensor(INPUT_1)
medMotor = MediumMotor(OUTPUT_B)

# Calibrate gyroscope
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)
tank.gyro = gs

count = 0
barVal = 0
while count < 4:
    movement.cartesian_move(0, 0.5, tank, [0, 0], 20)
    count += 1
    colVal = cs.value()
    # sound.speak(colVal)
    if colVal > 30:
        sound.speak("White")
        barVal += 1*(2**count);
    else:
        sound.speak("Black")
    sleep(0.5)

display.displayBarCode(barVal);
movement.turn(-90, tank, 20)
movement.cartesian_move(0, -2, tank, [0, 0], 20)
medMotor.on_for_degrees(30, 45)
movement.cartesian_move(0, 12, tank, [0, 0], 40)
