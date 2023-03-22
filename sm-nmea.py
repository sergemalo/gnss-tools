#!/usr/bin/python3
import sys
import version
from nmealib import nmea
from pathlib import PurePath

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
                if len(sys.argv)-1 > i:
                    self.file_name = sys.argv[i + 1]
                    ++i
                else:
                    raise RuntimeError("No file_name given with -f")
            ++i

def analyze_time(file_name: str):

    nmea_sentences = []

    # Open file
    with open(file_name) as f:
        for line in f:
            if (nmea.msg_type(line) == "RMC"):
                nmea_sentences.append(nmea.parse_GPRMC(line))

    if (nmea_sentences):
        print("Start time of NMEA file:", nmea_sentences[0].utc_datetime)

    # extract first GPRMC
    # scan file from the end
    # extract last GPRMC
    # Compute delta time and date

def unit_test():
    print()
    print("UNIT TEST")


# ______________________________________________________________________________
def main():
    version.print_version()
    opt = scriptOptions()
    opt.parse_argvs()

    if opt.help:
        opt.print_help()
        return

    if opt.unit_test:
        unit_test()
        return

    nmea.toto()

    analyze_time(opt.file_name)
main()
