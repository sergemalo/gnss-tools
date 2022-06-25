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
    
  def toString(self):
    return "Lat=" + str(self.lat) + "; Long=" + str(self.long) + "; Alt=" + str(self.alt)

  def equal(self, pos):
    return math.isclose(self.lat, pos.lat, abs_tol=0.00001) and \
      math.isclose(self.long, pos.long, abs_tol=0.00001) and \
      math.isclose(self.alt, pos.alt, abs_tol=0.00001)

def printVersion():
  print("Platform       : " + platform.system())
  print("Python version : " + platform.python_version())


class GPGGASentence:
 
  def __init__(self, utcTime = 0.0, lat = 0.0, long = 0.0, fixQual = 0, nbSat = 0, hdop = 0.0, alt = 0.0, heightGeoid = 0.0, timeDGPS = 0, dGPSRefId = 0):
    self.utcTime = utcTime
    self.lat = lat
    self.long = long
    self.fixQual = fixQual
    self.nbSat = nbSat
    self.hdop = hdop
    self.alt = alt
    self.heightGeoid = heightGeoid
    self.timeDGPS = timeDGPS
    self.dGPSRefId = dGPSRefId

  def toString(self):
    return "Lat=" + str(self.lat) + "; Long=" + str(self.long) + "; Alt=" + str(self.alt)


def parseArgs():
  
  #print (sys.argv)
  opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
  
  unitTest = False
  if '-t' in opts: unitTest = True
  return unitTest


# GPGGA: Global Positioning System Fix Data
def parseGPGGA(inSentence):
  print (inSentence)
  
  fields = re.split(r'\,', inSentence) 
  print (fields)
  if (fields[0] != "$GPGGA"):
    raise ("Sentence is not GPGGA")
  
  parsedGPGGA = GPGGASentence()
  
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

def unitTestGPGGA(sentence, expectedPos):
  parsedPos = Position()

  print ("Parsing NMEA...")
  print (sentence);

  parsedGPGGA = parseGPGGA(sentence)
  parsedPos.lat = parsedGPGGA.lat
  parsedPos.long = parsedGPGGA.long
  parsedPos.alt = parsedGPGGA.alt
  
  
  if (expectedPos.equal(parsedPos)):
    return True
  
  print ("Expected: "+ expectedPos.toString())
  print ("Parsed  : "+ parsedPos.toString())
  return False;


def unitTest():
  print ("UNIT TEST")
  
  expectedPos = Position(-43.1234, -73.0, 2.0)
  if (unitTestGPGGA("$GPGGA,120000.000,4307.4040,S,07300.0000,W,1,9,0.91,2.0,M,,M,,*55", expectedPos) == False):
    return False
  expectedPos = Position(37.387458333, -121.97236, 9.0)
  if (unitTestGPGGA("$GPGGA, 161229.487, 3723.2475, N, 12158.3416, W, 1, 07, 1.0, 9.0, M, , , , 0000*18", expectedPos) == False):
    return False

  print ("UNIT TEST PASS")
  return True
#______________________________________________________________________________
def main():
  printVersion()
  test = parseArgs()
  
  if (test == True):
    if (unitTest() == False):
      print ("UNIT TEST FAIL!")
    
    
    
    
    
    
main()
