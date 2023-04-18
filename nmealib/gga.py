import re

# https://docs.novatel.com/OEM7/Content/Logs/GGA.htm
# Example:
# $GGA,202530.00,5109.0262,N,11401.8407,W,5,40,0.5,1097.36,M,-17.00,M,18,TSTR*61


# Convert Degrees'Minute to decimal helper function
# 3723.2475
# DDMM.MMMM
def minutes_to_decimal(minutes_mantissa: int, minutes_frac: float):
    return (minutes_mantissa + minutes_frac) / 60.0

class GGASentence:
    def __init__(
        self,
        utcTime=0.0,
        lat=0.0,
        long=0.0,
        fixQual=0,
        nbSat=0,
        hdop=0.0,
        alt=0.0,
        heightGeoid=0.0,
        timeDGPS=0,
        dGPSRefId=0,
    ):
        self.utcTime = (
            utcTime  # Stored as seconds since the beginning of the day (float)
        )
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
        return (
            "Lat="
            + str(self.lat)
            + "; Long="
            + str(self.long)
            + "; Alt="
            + str(self.alt)
        )


# GGA: Global Positioning System Fix Data
def parse_GGA(inSentence):
    fields = re.split(r"\,", inSentence)
    if fields and fields[0][3:6] != "GGA":
        raise TypeError("Sentence is not NMEA XXGGA")

    parsedGGA = GGASentence()
    utcTime = re.match(r"\s*(\d{1,2})(\d{2})(\d{2}\.\d*)", fields[1])
    if utcTime is None:
        raise RuntimeError("Unable to parse UTC Time")
    parsedGGA.utcTime = float(utcTime.group(1)) * 3600.0
    parsedGGA.utcTime = parsedGGA.utcTime + float(utcTime.group(2)) * 60.0
    parsedGGA.utcTime = parsedGGA.utcTime + float(utcTime.group(3))

    latitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d+)", fields[2])
    if latitude is None:
        raise RuntimeError("Unable to parse Latitude")
    parsedGGA.lat = float(latitude.group(1))
    parsedGGA.lat = parsedGGA.lat + minutes_to_decimal(
        int(latitude.group(2)), float(latitude.group(4)) / (10.0 ** len(latitude.group(4)))
    )
    if fields[3] == "S":
        parsedGGA.lat = -parsedGGA.lat

    longitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d+)", fields[4])
    if longitude is None:
        raise RuntimeError("Unable to parse Longitude")
    parsedGGA.long = float(longitude.group(1))
    parsedGGA.long = parsedGGA.long + minutes_to_decimal(
        int(longitude.group(2)), float(longitude.group(4)) / (10 ** len(longitude.group(4)))
    )

    west = re.match(r"\s*(\w+)", fields[5])
    if west.group(1) == "W":
        parsedGGA.long = -parsedGGA.long

    parsedGGA.hdop = float(fields[8])
    parsedGGA.alt = float(fields[9])

    return parsedGGA

