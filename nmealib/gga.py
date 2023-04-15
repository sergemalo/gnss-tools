import re

# https://docs.novatel.com/OEM7/Content/Logs/GPGGA.htm
# Example:
# $GPGGA,202530.00,5109.0262,N,11401.8407,W,5,40,0.5,1097.36,M,-17.00,M,18,TSTR*61


# Convert Degrees'Minute to decimal helper function
# 3723.2475
# DDMM.MMMM
def minutes_to_decimal(minutes_mantissa: int, minutes_frac: int):
    return (minutes_mantissa + minutes_frac / 10000.0) / 60.0

class GPGGASentence:
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


# GPGGA: Global Positioning System Fix Data
def parse_GPGGA(inSentence):
    fields = re.split(r"\,", inSentence)
    if fields and fields[0][3:6] != "GGA":
        raise TypeError("Sentence is not NMEA XXGGA")

    parsedGPGGA = GPGGASentence()
    utcTime = re.match(r"\s*(\d{1,2})(\d{2})(\d{2}\.\d*)", fields[1])
    if utcTime is None:
        raise RuntimeError("Unable to parse UTC Time")
    parsedGPGGA.utcTime = float(utcTime.group(1)) * 3600.0
    parsedGPGGA.utcTime = parsedGPGGA.utcTime + float(utcTime.group(2)) * 60.0
    parsedGPGGA.utcTime = parsedGPGGA.utcTime + float(utcTime.group(3))

    latitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d{4})", fields[2])
    if latitude is None:
        raise RuntimeError("Unable to parse Latitude")
    parsedGPGGA.lat = float(latitude.group(1))
    parsedGPGGA.lat = parsedGPGGA.lat + minutes_to_decimal(
        int(latitude.group(2)), int(latitude.group(4))
    )
    if fields[3] == "S":
        parsedGPGGA.lat = -parsedGPGGA.lat

    longitude = re.match(r"\s*(\d{1,3})(\d{2})(\.)(\d{4})", fields[4])
    if longitude is None:
        raise RuntimeError("Unable to parse Longitude")
    parsedGPGGA.long = float(longitude.group(1))
    parsedGPGGA.long = parsedGPGGA.long + minutes_to_decimal(
        int(longitude.group(2)), int(longitude.group(4))
    )

    west = re.match(r"\s*(\w+)", fields[5])
    if west.group(1) == "W":
        parsedGPGGA.long = -parsedGPGGA.long

    parsedGPGGA.hdop = float(fields[8])
    parsedGPGGA.alt = float(fields[9])

    return parsedGPGGA

