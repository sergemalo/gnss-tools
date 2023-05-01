#!/usr/bin/python3
import sys
import version
from nmealib import nmea, RMCSentence, parse_RMC, GGASentence, parse_GGA, PosLLA, XYPoint, xy_dist
from pathlib import PurePath
from datetime import timedelta
from numpy import std, average, mean, square, median, quantile
from math import sqrt
import matplotlib.pyplot as plt

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
        for line in f: # Throws UnicodeDecodeError when binary data is parsed :-/
            if (nmea.msg_type(line) == "RMC"):
                nmea_sentences.append(parse_RMC(line))
            elif (nmea.msg_type(line) == "GGA"):
                nmea_sentences.append(parse_GGA(line))

    return nmea_sentences


def load_nmea_file2(file_name: str):
    nmea_sentences = []

    with open(file_name, 'rb') as f:
        all_lines = f.read().split(b'\n')
        print("Nb lines: ", len(all_lines))
        for l in all_lines:
            try:
                s = l.decode('utf-8')
            except UnicodeDecodeError:
                pass
                #print("Skipping binary data")
            #print(s)
            if (nmea.is_nmea(s)):
                #print("NMEA:", s)
                if (nmea.msg_type(s) == "RMC"):
                    nmea_sentences.append(parse_RMC(s))
                elif (nmea.msg_type(s) == "GGA"):
                    nmea_sentences.append(parse_GGA(s))

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
        i -= 1

    duration = timedelta(0)
    if first_rmc != last_rmc:
        print("End time of NMEA file:", last_rmc.utc_datetime)
        duration = last_rmc.utc_datetime - first_rmc.utc_datetime
        print("Duration of NMEA file:", duration)

    return duration

def cep(nmea_sentences: list):
    # Convert all GGP positions to X,Y
    xy_positions = []
    for line in nmea_sentences:
        if type(line) == GGASentence:
            lla = PosLLA(line.lat, line.long, line.alt)
            xy_positions.append(lla.to_xy())
    # Compute Average position
    avg_xy_pos = XYPoint(sum([p.x for p in xy_positions])/len(xy_positions), sum([p.y for p in xy_positions])/len(xy_positions))


    print ("Average XY PosLLA: ", avg_xy_pos)

    distances = []
    for p in xy_positions:
        distances.append(xy_dist(p, avg_xy_pos))

    #for d in distances:
    #    print("{:.15}".format(d))

    print("Standard Deviation: {:.3f} m".format(std(distances)))
    print("Average error: {:.3f} m".format(average(distances)))
    print("Mean error: {:.3f} m".format(mean(distances)))
    print("RMS error: {:.3f} m".format( sqrt(mean(square(distances) ) ) ) )
    print("2dRMS error: {:.3f} m".format( 2*sqrt(mean(square(distances) ) ) ) )
    cep = median(distances)
    print("CEP (median): {:.3f} m".format(cep))

    r95 = quantile(distances, 0.95)
    print("R95: {:.3f} m".format(r95))

    plot_cep(xy_positions, avg_xy_pos, max(distances), cep, r95)

def plot_cep(positions, center, max_distance, cep, r95):

    # Use OO API of matplotlib
    fig, ax = plt.subplots()

    # Make sure Axes width/height are equal,
    # because we want the CEP cirle to be a circle, not an oval.
    ax.set_aspect(aspect='equal')
    ax.set_xlabel('x in meters')
    ax.set_ylabel('y in meters')
    ax.set_title('Circular Error Probable (CEP)')
    ax.set_xlim(-max_distance, max_distance)
    ax.set_ylim(-max_distance, max_distance)

    # TBD: is this the best way to draw a circle on the Axes ?
    circle1 = plt.Circle((0, 0), cep, color='b', fill=False, label='CEP = {:.3f} m'.format(cep))
    ax.add_patch(circle1)
    circle2 = plt.Circle((0, 0), r95, color='r', fill=False, label='R95 = {:.3f} m'.format(r95))
    ax.add_patch(circle2)

    xs = []
    ys = []
    for p in positions:
        xs.append(p.x - center.x)
    for p in positions:
        ys.append(p.y - center.y)
    ax.scatter(xs, ys, s=1, facecolor='C0', edgecolor='k')
    ax.legend()

    plt.show()


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

    nmea_sentences = load_nmea_file2(opt.file_name)
    if (len(nmea_sentences) < 2):
        print("Less than 2 NMEA sentences detected - no analysis to perform")
        return
    analyze_time_rmc(nmea_sentences)
    cep(nmea_sentences)

    ##
    # sep - convert LLA to XYZ (3D)
    ## plot in 3D
    ## Move functions to NMEA lib
    ## class nmea file
    ##    Parse all sentences on open - Optimize later if needed
    ##    Get all positions
    ##    Get start/end time
    ## function to compute
    ##    Average position
    ##    All precision / accuracy


main()
