#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import OUTPUT_A, MoveTank, OUTPUT_D
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sound import Sound
import movement


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
gs = GyroSensor(INPUT_1)

# Calibrate gyroscope
sound.speak("Calibrating, do not touch mindstorm.")
sleep(1)
gs.calibrate()
sound.speak("Calibration complete.")
sleep(1)
tank.gyro = gs

# Subtask 1A
# movement.SubTask1A(30, 10, tank, gs) # Produces error of 4.4.166667cm x, 2.666667cm y

# Subtask 1B
pos=[0,0]
movement.cartesian_move(50, 50, tank, pos)
sound.speak("Please move robot back to original position.")
sound.speak("Robot should move to the same position it previously moved to, if it does not please alert lead programmer.")
sleep(10)
movement.vector_move(50, 50, tank, pos)
sound.speak("Current position should be 100, 100")
print("current position is: ", pos[0], ", ", pos[1])
sound.speak("If these positions differ please alert lead programmer.")
sound.speak("Should return to original position if it does not, please alart lead programmer.")
movement.vector_move(-50, -50, tank, pos)
sound.speak("Current position should be 50, 50")
print("current position is: ", pos[0], ", ", pos[1])
sound.speak("If these positions differ please alert lead programmer.")
