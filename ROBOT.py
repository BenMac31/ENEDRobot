#!/usr/bin/env python3

from time import sleep
import statistics
import math
import random

from ev3dev2.motor import\
    OUTPUT_A,\
    OUTPUT_B,\
    OUTPUT_D,\
    SpeedPercent,\
    MoveTank,\
    MediumMotor,\
    LargeMotor
from ev3dev2.sensor import\
        INPUT_1,\
        INPUT_2,\
        INPUT_3
from ev3dev2.sensor.lego import\
        GyroSensor,\
        UltrasonicSensor,\
        ColorSensor
# from ev3dev2.led import Leds
from ev3dev2.sound import Sound

import display


# Calibrate gyroscope
class Robot:
    t = None
    gy = None
    cs = None
    mm = None
    s = None
    pos = [0, 0, 0]
    rm = None
    lm = None
    moveCalibrate = 0.44444366439024386
    armCalibrate = 19
    defaultPower = 50
    expectedBarcode = None
    foundBarcode = None
    correctBarcode = True
    usLock = False

    backendPos = 0
    backendPosMod = 0

    BoxToPickup = ["NA", 0]
    home = "A"

    boxStyle = "normal"

    def __init__(self,
                 features=[], all=False,
                 home="A"):
        global t, gy, cs, mm, s
        if all or len(features) == 0:
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
                self.gy.calibrate()
                self.s.speak("Calibration complete.")
                if self.t:
                    self.t.gyro = self.gy
            if i == "colour":
                self.cs = ColorSensor(INPUT_3)
                self.s.speak(
                        "Callibrating white,"
                        "please put white infront of color sensor"
                        )
                sleep(3)
                self.cs.calibrate_white()
                self.s.speak(
                        "Calibration complete.",
                        play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE
                        )
                if self.t:
                    self.t.gyro = self.gy
            if i == "us":
                self.us = UltrasonicSensor(INPUT_2)
            if i == "medMotor":
                self.mm = MediumMotor(OUTPUT_B)
        self.home = home
        self.pos = self.pos_from_home(home)

    def pos_from_home(self, home):
        if home == "A":
            pos = [6, -6, 0]
        elif home == "B":
            pos = [102, -6, 0]
        elif home == "C":
            pos = [6, 114, 180]
        elif home == "D":
            pos = [102, 114, 180]
        else:
            raise ValueError("Invalid Home")
        return pos

    def check_move(self, *args, **kwargs) -> bool:
        distance = kwargs["distance"]
        useUS = kwargs["useUS"]
        self.backendPos =\
            ((self.rm.rotations+self.lm.rotations)/2) - self.backendPosMod
        if abs(self.backendPos) > abs(distance):
            self.backendPosMod += self.backendPos
            return False
        elif (useUS):
            obsDistance = self.us.distance_inches
            if (obsDistance < 12):
                print("Obstacle distance:" +
                      str(int(obsDistance)) +
                      " inches.")
                self.usLock = True
                self.backendPosMod += self.backendPos
                return False
            else:
                return True
        else:
            return True

    def move(self, inch: float, power=0, useUS=True):
        """Moves 'inch' inch forward (backwards is negative.)"""

        if inch == 0:
            return

        if power == 0:
            power = self.defaultPower

        if inch < 0:
            useUS = False
            power *= -1

        self.backendPosMod = 0
        self.backendPos = 0
        self.rm.position = 0
        self.lm.position = 0

        dist=inch
        while True:
            self.t.follow_gyro_angle(
                kp=11.3, ki=0.05, kd=3.2,
                speed=SpeedPercent(power),
                target_angle=self.pos[2],
                sleep_time=0.01,
                follow_for=self.check_move,
                distance=dist*self.moveCalibrate,
                useUS=useUS
            )
            if self.usLock:
                while self.usLock:
                    sleep(0.1)
                    self.usLock = self.us.distance_inches < 12
                dist-=self.backendPosMod*self.moveCalibrate
                print("Moved " + str(self.backendPosMod*self.moveCalibrate) + " inches.")
                print("Distand Reamining" + str(dist) + " inches.")
            else:
                break

        self.pos = [
                self.pos[0] + inch*round(math.cos((90*math.pi)/180), 10),
                self.pos[1] + inch*round(math.sin((90*math.pi)/180), 10),
                self.pos[2]]
        sleep(0.1)

    def turn(self, degrees: float, power=0):
        """Turns 'degrees' degrees clockwise (counterclockwise is negative.)"""

        if power == 0:
            power = self.defaultPower/2

        self.t.turn_degrees(
            speed=SpeedPercent(power),
            error_margin=1,
            target_angle=degrees,
        )

        self.pos[2] = self.pos[2]+degrees

    def parse_input_barcode(self, barcode: str):
        """Parses an input barcode into the expected format of a 4 bit
        unsigned integer.
        EX: (# # ) becomes 10"""
        outputNumber = 0
        if len(barcode) == 4:
            for i in range(4):
                if barcode[i] == " ":
                    outputNumber += 2**i
        else:
            raise ValueError("Barcode is not 4 characters long.")
        self.expectedBarcode = outputNumber
        return outputNumber

    def validate_barcode(self, speak=True):
        """Validates the barcode that was scanned."""
        if self.expectedBarcode == self.foundBarcode:
            if speak:
                self.s.speak(
                        "Barcode is correct.",
                        play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            return True
        else:
            if speak:
                self.s.speak(
                        "Barcode is incorrect.",
                        play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)
            return False

    def turn_arm_degrees(self, degrees, power=30):
        """Turns the arm a certain amount of degrees."""
        power *= -1 if degrees < 0 else 1
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

    def scan_barcode(self, pickup=False, validate=False, showBarcode=True):
        barVal = 0
        cols = [0 for _ in range(4)]
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
            display.displayBarCode(barVal)
        if validate:
            self.validate_barcode()
        if (pickup and self.correctBarcode):
            self.pickup()

    def move_to_pos(self, pos, power=0):
        """Moves to a specified position."""

        if power == 0:
            power = self.defaultPower

        if self.pos[2] % 180 == 0:
            if pos[1] != 0:
                if self.pos[2] == 180:
                    y = self.pos[1]-pos[1]
                else:
                    y = pos[1]-self.pos[1]
                self.move(y, power)
            if pos[0] != 0:
                turnDir = (pos[0] < 0)*-2+1
                self.turn(90*turnDir, power)
                self.move(pos[0])
        else:
            if pos[0] != 0:
                if self.pos[2] == 180:
                    x = self.pos[0]-pos[0]
                else:
                    x = pos[0]-self.pos[0]
                self.move(x, power)
            if pos[1] != 0:
                turnDir = (pos[0] < 0)*-2+1
                self.turn(90*turnDir, power)
                self.move(pos[1])

    def set_loc(self, list):
        """Reads the first item of list (should be a string), as the shelf, and
        the second item as the item."""
        if len(list) == 2:
            self.BoxToPickup[0] = list[0]
            self.BoxToPickup[1] = list[1]
        else:
            raise ValueError("List is not 2 items long.")

    def move_to_shelf(self, shelf, side):
        if shelf == "A1":
            self.move_to_pos([6, 16+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "A2":
            self.move_to_pos([6, 42+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "C1":
            self.move_to_pos([6, 66+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "C2":
            self.move_to_pos([6, 90+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "B1":
            self.move_to_pos([60, 16+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "B2":
            self.move_to_pos([60, 42+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "D1":
            self.move_to_pos([60, 66+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))
        elif shelf == "D2":
            self.move_to_pos([60, 90+6*(-1+(2*side))])
            self.turn(90*(-1+(2*side)))

    def move_to_unit(self, unit):
        if self.boxStyle == "normal":
            self.move((3+6*((12-1) % 6)-(59/16)))

    def move_to_loc(self, loc=None):
        """Moves to location specified"""

        if loc is not None:
            self.set_loc(loc)

        if loc[1] > 6:
            side = False
        else:
            side = True

        self.move_to_shelf(loc[0], side)
        self.move_to_unit(loc[1])

    def move_to_home(self, home, atHome=True, power = 0):
        """Moves to specified home location"""

        if power == 0:
            power = self.defaultPower

        if atHome:
            self.move(12)
            if self.home == "A":
                if home == "D":
                    self.turn(90, power)
                    self.move(96, power)
                    self.turn(-90, power)
                    self.move(108, power)
                if home == "C":
                    self.move(108, power)
                if home == "B":
                    self.turn(90, power)
                    self.move(96, power)
                    self.turn(-90, power)
                    self.move(12, power)
            elif self.home == "B":
                if home == "C":
                    self.turn(-90, power)
                    self.move(96, power)
                    self.turn(90, power)
                    self.move(108, power)
                if home == "D":
                    self.move(108, power)
                if home == "A":
                    self.turn(-90, power)
                    self.move(96, power)
                    self.turn(90, power)
                    self.move(-12, power)
            elif self.home == "C":
                if home == "B":
                    self.turn(90, power)
                    self.move(96, power)
                    self.turn(-90, power)
                    self.move(108, power)
                if home == "A":
                    self.move(108, power)
                if home == "D":
                    self.turn(90, power)
                    self.move(96, power)
                    self.turn(-90, power)
                    self.move(12, power)
            elif self.home == "D":
                if home == "A":
                    self.turn(-90, power)
                    self.move(96, power)
                    self.turn(90, power)
                    self.move(108, power)
                if home == "B":
                    self.move(108, power)
                if home == "C":
                    self.turn(-90, power)
                    self.move(96, power)
                    self.turn(90, power)
                    self.move(12, power)
        else:
            self.move_to_pos(self.pos_from_home(home))
        self.home = home

    def auto_calibrate(self):
        """Automatically calibrates the robot moveCalibrate by moving 12 inches
        forward, and comparing the expected movement to the distance changed
        from the ultraSonics measurements."""
        calibrations = []
        calibrations.append(self.moveCalibrate)
        while True:
            distanceToTravel = random.randint(1, 24)
            sleep(3)
            distanceToWall = self.us.distance_inches
            print("Angle: " + str(self.gy.angle) + " degrees.")
            print("Distance to travel: " + str(distanceToTravel) + " inches.")
            print("Distance to wall: " + str(distanceToWall) + " inches.")
            self.move(distanceToTravel, useUS=False)
            sleep(3)
            newDistanceToWall = self.us.distance_inches
            realDistanceMoved = distanceToWall-newDistanceToWall
            print("New distance to wall: "
                  + str(newDistanceToWall)
                  + " inches.")
            print("Real distance moved: "
                  + str(realDistanceMoved)
                  + " inches.")
            calibrations.append(
                    self.moveCalibrate/(realDistanceMoved/distanceToTravel))
            newMoveCalibrate = statistics.mean(calibrations)
            print("Better moveCalibrate: " + str(newMoveCalibrate))
            self.move(-distanceToTravel, useUS=False)
            self.moveCalibrate = newMoveCalibrate
