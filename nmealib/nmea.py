import re
import math

def toto():
    print("TOTO")

def talker_id(nmea_sentence: str):
    if nmea_sentence[0] != "$":
        raise RuntimeError("Invalid NMEA sentence")
    if len(nmea_sentence) < 6:
        raise RuntimeError("Invalid NMEA sentence")
    return nmea_sentence[1:3]

def msg_type(nmea_sentence: str):
    if nmea_sentence[0] != "$":
        raise RuntimeError("Invalid NMEA sentence")
    if len(nmea_sentence) < 6:
        raise RuntimeError("Invalid NMEA sentence")
    return nmea_sentence[3:6]

# NMEA example:
# 3723.2475
# DDMM.MMMM
#class CoordDMS:
#    def __init__(self, degrees, minutes, factional_minutes):

def minutes_to_decimal(minutes_mantissa : int, minutes_frac: int):
    return (minutes_mantissa + minutes_frac/10000.0)/60.0

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
  parsedGPGGA.lat = parsedGPGGA.lat + minutes_to_decimal(int(latitude.group(2)), int(latitude.group(4)))
  #parsedGPGGA.lat = parsedGPGGA.lat + (float(latitude.group(2)) + float(latitude.group(4) )/10000.0 )/60.0
  if (fields[3] == "S"):
      parsedGPGGA.lat = -parsedGPGGA.lat

  longitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d{4})", fields[4])
  if (longitude == None):
    raise ("Unable to parse Longitude")
  parsedGPGGA.long = float(longitude.group(1))
  parsedGPGGA.long = parsedGPGGA.long + minutes_to_decimal(int(longitude.group(2)), int(longitude.group(4)))
  #parsedGPGGA.long = parsedGPGGA.long + (float(longitude.group(2)) + float(longitude.group(4) )/10000.0 )/60.0

  west = re.match(r"\s*(\w+)", fields[5])
  if (west.group(1) == "W"):
      parsedGPGGA.long = -parsedGPGGA.long

  parsedGPGGA.hdop  = float(fields[8])
  parsedGPGGA.alt  = float(fields[9])

  return parsedGPGGA

