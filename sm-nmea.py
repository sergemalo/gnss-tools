#!/usr/bin/python3
import sys
import version
from nmealib import nmea, RMCSentence, parse_GPRMC
from pathlib import PurePath
from datetime import timedelta

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

def load_nmea_file(file_name: str):
    nmea_sentences = []

    with open(file_name) as f:
        for line in f:
            if (nmea.msg_type(line) == "RMC"):
                nmea_sentences.append(parse_GPRMC(line))

    return nmea_sentences

def analyze_time_rmc(nmea_sentences: list):

    first_rmc = None
    last_rmc = None
    for s in nmea_sentences:
        if type(s) == RMCSentence:
            first_rmc = s
            break

    if not first_rmc:
        print("Cannot analyze time based on RMC sentences: No RMC sentence found")
        return

    print("Start time of NMEA file:", first_rmc.utc_datetime)

    i = len(nmea_sentences) - 1
    while (i >= 0):
        if type(nmea_sentences[i]) == RMCSentence:
            last_rmc = nmea_sentences[i]
            break

    duration = timedelta(0)
    if first_rmc != last_rmc:
        print("End time of NMEA file:", last_rmc.utc_datetime)
        duration = last_rmc.utc_datetime - first_rmc.utc_datetime
        print("Duration of NMEA file:", duration)

    return duration

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

    nmea_sentences = load_nmea_file(opt.file_name)
    analyze_time_rmc(nmea_sentences)

main()
