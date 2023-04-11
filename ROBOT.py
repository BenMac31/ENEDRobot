#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MoveDifferential, SpeedRPM, MediumMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import TouchSensor, GyroSensor, UltrasonicSensor, ColorSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import math
import movement
from ev3dev2.wheel import EV3EducationSetRim


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
gs = GyroSensor(INPUT_1)

# Calibrate gyroscope
class Robot:
    t : MoveTank
    gy : GyroSensor
    cs : ColorSensor
    mm : MediumMotor
    s : Sound
    pos = None;
    moveCalibrate : float = 0;
    defaultPower : int = 0;

    def __init__(self, features = [], all = False, moveCalibrate = 0.4313007, defaultPower = 50):
        global t, gy, cs, mm, s
        if all == True or len(features) == 0:
            features = ["move", "gyro", "us", "colour", "medMotor"]
        self.s = Sound()
        for i in features:
            if i == "move":
                self.t = MoveTank(OUTPUT_A, OUTPUT_D)
                if self.gy:
                    self.t.gyro = self.gy
            if i == "gyro":
                self.gy = GyroSensor(INPUT_1)
                self.s.speak("Callibrating gyroscope, do not touch mindstorm.")
                self.gy.calibrate();
                sound.speak("Calibration complete.", play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                if self.t:
                    self.t.gyro = self.gy
            if i == "colour":
                self.cs = ColorSensor(INPUT_3)
                self.s.speak("Callibrating white, please put white infront of color sensor")
                sleep(3)
                self.cs.calibrate_white()
                sound.speak("Calibration complete.", play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                if self.t:
                    self.t.gyro = self.gy
            if i == "us":
                self.us = UltrasonicSensor(INPUT_2)
            if i == "medMotor":
                self.mm = MediumMotor(OUTPUT_B)
        self.pos = [0, 0]
        self.moveCalibrate = moveCalibrate
        self.defaultPower = defaultPower

    def move(self, inch : float, power = defaultPower):
        """Moves 'inch' inch forward (backwards is negative.)"""
        inch *= self.moveCalibrate

        self.t.on_for_rotations(
                SpeedPercent(power), SpeedPercent(power), inch
                )

    def turn(self, degrees : float, power = defaultPower):
        """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""
        self.t.turn_degrees(
            speed=SpeedPercent(-power),
            target_angle=degrees,
        )

    def cartesian_move(self, x, y, power = defaultPower):
        """Moves to an x and y location by first moving to the y position, then turning 90 degrees and moving to the x location."""
        if y!=0:
            self.move(y, power)
        if x!=0:
            turnDir=(x < 0)*-2+1
            self.turn(90*turnDir, power)
    
