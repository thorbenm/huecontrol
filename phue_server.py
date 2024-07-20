#!/usr/bin/python3
import motionsensor
import switch
from time import sleep


def main():
    while True:
        motionsensor.update()
        switch.update()
        sleep(.5)


if __name__ == '__main__':
    main()
