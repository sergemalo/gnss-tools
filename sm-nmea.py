#!/usr/bin/python3
import sys
import platform
from pathlib import PurePath

# import nmea


def printVersion():
    print("Platform       : " + platform.system())
    print("Python version : " + platform.python_version())


class scriptOptions:
    def __init__(self):
        self.unit_test = False
        self.help = False
        self.file_name = None

    def print_help(self):
        print()
        print(PurePath(sys.argv[0]).name, " options:")
        # print("{0} options:".format((PurePath(sys.argv[0])).name)
        print("  -t           :  Unit testing this script")
        print("  -f file_name :  Input NMEA file name")

    def parse_argvs(self):
        # print (sys.argv)
        i = 1
        for a in sys.argv[1:]:
            if a == "-h":
                self.help = True
            if a == "-t":
                self.unit_test = True
            if a == "-f":
                if len(sys.argv) > i:
                    self.file_name = sys.argv[i + 1]
                    ++i
                else:
                    raise RuntimeError("No file_name given with -f")
            ++i


def unit_test():
    print()
    print("UNIT TEST")


# ______________________________________________________________________________
def main():
    printVersion()
    opt = scriptOptions()
    opt.parse_argvs()

    if opt.help:
        opt.print_help()
        return

    if opt.unit_test:
        unit_test()
        return


main()
