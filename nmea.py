#!/usr/bin/python3
import sys
import platform
import re
import math

# Position Class:
# Values are stored in decimal, in floating-point attributes (Python's float is a double-precision C++)
# Latitude range : [-90.0, +90.0]
# Longitude range: [-180.0, +180.0]
# Altitude range: [-Infinite, +Infinite]
class Position:
  def __init__(self, lat=0.0, long=0.0, alt=0.0):
    self.lat = lat
    self.long = long
    self.alt = alt

    @property
    def lat(self):
        return self._lat
    @lat.setter
    def lat(self, value):
        if (value < -90.0) or (value > 90.0):
            raise ValueError("Latitude value must be between -90.0 and +90.0 degrees")
        else:
            self._lat = value

    @property
    def long(self):
        return self._long
    @long.setter
    def long(self, value):
        if (value < -180.0) or (value > 180.0):
            raise ValueError("Longitude value must be between -180.0 and +180.0 degrees")
        else:
            self._long = value

    @property
    def alt(self):
        return self._alt
    @alt.setter
    def alt(self, value):
        self._alt = value


  def __str__(self):
    return "Lat=" + str(self.lat) + "; Long=" + str(self.long) + "; Alt=" + str(self.alt)

  def __eq__(self, pos):
    return math.isclose(self.lat, pos.lat, abs_tol=0.00001) and \
      math.isclose(self.long, pos.long, abs_tol=0.00001) and \
      math.isclose(self.alt, pos.alt, abs_tol=0.00001)

def print_version():
  print("Platform       : " + platform.system())
  print("Python version : " + platform.python_version())


class GPGGASentence:

  def __init__(self, utcTime = 0.0, lat = 0.0, long = 0.0, fixQual = 0, nbSat = 0, hdop = 0.0, alt = 0.0, heightGeoid = 0.0, timeDGPS = 0, dGPSRefId = 0):
    self.utcTime = utcTime  # Stored as seconds since the beginning of the day (float)
    self.lat = lat
    self.long = long
    self.fixQual = fixQual
    self.nbSat = nbSat
    self.hdop = hdop
    self.alt = alt
    self.heightGeoid = heightGeoid
    self.timeDGPS = timeDGPS
    self.dGPSRefId = dGPSRefId

  def __str__(self):
    return "Lat=" + str(self.lat) + "; Long=" + str(self.long) + "; Alt=" + str(self.alt)


def parse_args():

  #print (sys.argv)
  opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]

  unitTest = False
  if '-t' in opts: unitTest = True
  return unitTest


# GPGGA: Global Positioning System Fix Data
def parse_GPGGA(inSentence):
  fields = re.split(r'\,', inSentence)
  if (fields[0] != "$GPGGA"):
    raise ("Sentence is not GPGGA")

  parsedGPGGA = GPGGASentence()

  utcTime = re.match(r"\s*(\d{1,2})(\d{2})(\d{2}\.\d*)", fields[1])
  if (utcTime == None):
    raise ("Unable to parse UTC Time")
  parsedGPGGA.utcTime = float(utcTime.group(1)) * 3600.0
  parsedGPGGA.utcTime = parsedGPGGA.utcTime + float(utcTime.group(2)) * 60.0
  parsedGPGGA.utcTime = parsedGPGGA.utcTime + float(utcTime.group(3))


  latitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d{4})", fields[2])
  if (latitude == None):
    raise ("Unable to parse Latitude")
  parsedGPGGA.lat = float(latitude.group(1))
  parsedGPGGA.lat = parsedGPGGA.lat + (float(latitude.group(2)) + float(latitude.group(4) )/10000.0 )/60.0
  if (fields[3] == "S"):
      parsedGPGGA.lat = -parsedGPGGA.lat

  longitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d{4})", fields[4])
  if (longitude == None):
    raise ("Unable to parse Longitude")
  parsedGPGGA.long = float(longitude.group(1))
  parsedGPGGA.long = parsedGPGGA.long + (float(longitude.group(2)) + float(longitude.group(4) )/10000.0 )/60.0

  west = re.match(r"\s*(\w+)", fields[5])
  if (west.group(1) == "W"):
      parsedGPGGA.long = -parsedGPGGA.long

  parsedGPGGA.hdop  = float(fields[8])
  parsedGPGGA.alt  = float(fields[9])

  return parsedGPGGA

def unit_test_GPGGA(sentence, expectedTime, expectedPos):
  parsedPos = Position()

  print (sentence);

  parsedGPGGA = parse_GPGGA(sentence)
  parsedPos.lat = parsedGPGGA.lat
  parsedPos.long = parsedGPGGA.long
  parsedPos.alt = parsedGPGGA.alt

  if (not math.isclose(parsedGPGGA.utcTime, expectedTime, abs_tol=0.0000000001)):
    print ("Invalid UTC Time")
    print ("Expected: "+ str(expectedTime))
    print ("Parsed  : "+ str(parsedGPGGA.utcTime))
    return False

  if (expectedPos != (parsedPos)):
    print ("Invalid Position")
    print ("Expected: " + str(expectedPos))
    print ("Parsed  : " + str(parsedPos))
    return False

  return True;


def unit_test():
  print ("UNIT TEST")
  print ("Parsing NMEA...")

  expectedPos = Position(-43.1234, -73.0, 2.0)
  if (unit_test_GPGGA("$GPGGA,120000.000,4307.4040,S,07300.0000,W,1,9,0.91,2.0,M,,M,,*55", 12*3600.0, expectedPos) == False):
    return False
  expectedPos = Position(37.387458333, -121.97236, 9.0)
  if (unit_test_GPGGA("$GPGGA, 161229.487, 3723.2475, N, 12158.3416, W, 1, 07, 1.0, 9.0, M, , , , 0000*18", 16*3600.0 + 12*60.0 + 29.487, expectedPos) == False):
    return False
  expectedPos = Position(33.5705224283, -112.1842949, 354.682)
  if (unit_test_GPGGA("$GPGGA,001038.00,3334.2313457,N,11211.0576940,W,2,04,5.4,354.682,M,- 26.574,M,7.0,0138*79", 10*60.0 + 38.0, expectedPos) == False):
    return False





  print ("UNIT TEST PASS")
  return True
#______________________________________________________________________________
def main():
  print_version()
  test = parse_args()

  if (test == True):
    if (unit_test() == False):
      print ("UNIT TEST FAIL!")


main()
