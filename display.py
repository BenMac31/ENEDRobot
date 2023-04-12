#!/usr/bin/env python3

def displayBarCode(number, size=3):
    for i in range(size):
        for binary in '{0:04b}'.format(number):
            if binary == "1":
                print("#"*size, end='')
            else:
                print(" "*size, end='')
        print("\\n")
