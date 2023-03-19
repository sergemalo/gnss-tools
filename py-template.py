#!/usr/bin/python3
import sys
import platform


def printVersion():
    print("Platform       : " + platform.system())
    print("Python version : " + platform.python_version())


def parseArgs():

    # print (sys.argv)
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

    unitTest = False
    if "-t" in opts:
        unitTest = True
    return unitTest


def unitTest():
    print("UNIT TEST")


# ______________________________________________________________________________
def main():
    printVersion()
    test = parseArgs()

    if test == True:
        if unitTest() == False:
            print("UNIT TEST FAIL!")


main()
