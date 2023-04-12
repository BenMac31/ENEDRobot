#!/usr/bin/env python3

from time import sleep

from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank, OUTPUT_D, MediumMotor, LargeMotor
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor, ColorSensor
# from ev3dev2.led import Leds
from ev3dev2.sound import Sound
import statistics

import display


tank = MoveTank(OUTPUT_A, OUTPUT_D)
sound = Sound()
gs = GyroSensor(INPUT_1)

# Calibrate gyroscope
class Robot:
    t = None
    gy = None
    cs = None
    mm = None
    s = None
    pos = None
    rm = None
    lm = None
    moveCalibrate = 0
    armCalibrate = 0
    defaultPower = 0
    expectedBarcode = None
    foundBarcode = None
    correctBarcode = True
    usLock = False

    backendPos = 0
    backendPosMod = 0

    def __init__(self, features = [], all = False, moveCalibrate = 0.4313007, defaultPower = 50, armCalibrate = 19):
        global t, gy, cs, mm, s
        if all == True or len(features) == 0:
            features = ["move", "gyro", "us", "colour", "medMotor"]
        self.s = Sound()
        for i in features:
            if i == "move":
                self.t = MoveTank(OUTPUT_D, OUTPUT_A)
                self.rm = LargeMotor(OUTPUT_A)
                self.lm = LargeMotor(OUTPUT_D)
                if self.gy:
                    self.t.gyro = self.gy
            if i == "gyro":
                self.gy = GyroSensor(INPUT_1)
                self.s.speak("Callibrating gyroscope, do not touch mindstorm.")
                self.gy.calibrate();
                self.s.speak("Calibration complete.")
                if self.t:
                    self.t.gyro = self.gy
            if i == "colour":
                self.cs = ColorSensor(INPUT_3)
                self.s.speak("Callibrating white, please put white infront of color sensor")
                sleep(3)
                self.cs.calibrate_white()
                self.s.speak("Calibration complete.", play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
                if self.t:
                    self.t.gyro = self.gy
            if i == "us":
                self.us = UltrasonicSensor(INPUT_2)
            if i == "medMotor":
                self.mm = MediumMotor(OUTPUT_B)
        self.pos = [0, 0]
        self.moveCalibrate = moveCalibrate
        self.armCalibrate = armCalibrate
        self.defaultPower = defaultPower

    def check_move(self, *args, **kwargs) -> bool:
        distance = kwargs["distance"]
        useUS = kwargs["useUS"]
        self.backendPos = ((self.rm.rotations+self.lm.rotations)/2) - self.backendPosMod
        if abs(self.backendPos) > abs(distance):
            print("Travelled " + str(int((self.backendPos)/self.moveCalibrate)) + " inches.")
            self.backendPosMod += self.backendPos
            return False
        elif (useUS == True):
            obsDistance = self.us.distance_inches
            if (obsDistance < 12):
                print("Obstacle distance:" + str(int(obsDistance)) + " inches.")
                self.usLock = True
                self.backendPosMod += self.backendPos
                return False
            else:
                return True
        else:
            return True

    def move(self, inch : float, power = 0, useUS = True):
        """Moves 'inch' inch forward (backwards is negative.)"""

        if power == 0:
            power = self.defaultPower/2

        if inch < 0:
            useUS = False
            power*=-1

        self.t.follow_gyro_angle(
            kp=11.3, ki=0.05, kd=3.2,
            speed=SpeedPercent(power),
            target_angle=0,
            sleep_time=0.01,
            follow_for=self.check_move,
            distance = inch*self.moveCalibrate,
            useUS = useUS
        )

    def turn(self, degrees : float, power = 0):
        """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""

        if power == 0:
            power = self.defaultPower/2

        self.t.turn_degrees(
            speed=SpeedPercent(-power),
            error_margin=1,
            target_angle=degrees,
        )

    def cartesian_move(self, x, y, power = 0):
        """Moves to an x and y location by first moving to the y position, then turning 90 degrees and moving to the x location."""
        if power == 0:
            power = self.defaultPower

        if y!=0:
            self.move(y, power)
        if x!=0:
            turnDir=(x < 0)*-2+1
            self.turn(90*turnDir, power)

    def parse_input_barcode(self, barcode : str):
        """ Parses an input barcode (EX: '# # ') into the expected format of a 4 bit unsigned integer."""
        outputNumber = 0
        if len(barcode) == 4:
            for i in range(4):
                if barcode[i] == " ":
                    outputNumber += 2**i
        else:
            raise ValueError("Barcode is not 4 characters long.")
        self.expectedBarcode = outputNumber
        return outputNumber

    def validate_barcode(self, speak = True):
        """Validates the barcode that was scanned."""
        if self.expectedBarcode == self.foundBarcode:
            if speak:
                sound.speak("Barcode is correct.", play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            return True
        else:
            if speak:
                sound.speak("Barcode is incorrect.", play_type = Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            return False
    
    def turn_arm_degrees(self, degrees, power = 30):
        """Turns the arm a certain amount of degrees."""
        power*=-1 if degrees < 0 else 1
        degrees = abs(degrees)
        self.mm.on_for_rotations(power, degrees/self.armCalibrate)

    def pickup(self):
        # Movement logic for picking up the box
        self.defaultPower = 20
        self.move(2)
        self.turn(90)
        self.move(1)
        self.turn_arm_degrees(90)
        self.move(-2)
        self.turn_arm_degrees(-90)
        self.move(12)
        self.turn_arm_degrees(90)
        self.defaultPower = 50
        self.move(6)
        self.turn_arm_degrees(-90)


    def scan_barcode(self, pickup = False, validate = False, showBarcode = True):
        barVal = 0
        cols=[0 for _ in range(4)]
        for i in range(4):
            cols[i] = self.cs.value()
            sleep(0.1)
            self.move(0.5, 20)

        # Calculate barcode number
        colMax = max(cols)
        for i in range(len(cols)):
            if cols[i] < colMax - 20:
                barVal += 2**i
        self.foundBarcode = barVal

        if showBarcode:
            display.displayBarCode(barVal);
        if validate:
            self.validate_barcode()
        if (pickup and self.correctBarcode):
            self.pickup()

    def auto_calibrate(self):
        """Automatically calibrates the robot moveCalibrate by moving 12 inches forward, and comparing the expected movement to the distance changed from the ultraSonics measurements."""
        calibrations=[]
        calibrations.append(self.moveCalibrate)
        while True:
            sleep (3)
            distanceToWall = self.us.distance_inches
            print("Distance to wall:" + str(distanceToWall) + " inches.")
            self.move(12)
            sleep (3)
            newDistanceToWall = self.us.distance_inches
            realDistanceMoved = distanceToWall-newDistanceToWall
            print("New distance to wall:" + str(newDistanceToWall) + " inches.")
            print("Real distance moved:" + str(realDistanceMoved) + " inches.")
            calibrations.append(self.moveCalibrate/(realDistanceMoved/12))
            newMoveCalibrate = statistics.mean(calibrations)
            print("Better moveCalibrate: " + str(newMoveCalibrate))
            self.move(-12)
            self.moveCalibrate=newMoveCalibrate
