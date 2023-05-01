import math
from collections import namedtuple

EARTH_RADIUS = 6371008.8
ABSOLUTE_LAT_TOLERANCE = 0.001 / EARTH_RADIUS  # 1mm in Radians
ABSOLUTE_ALT_TOLERANCE = 0.001  # 1mm

XYPoint = namedtuple("XYPoint", "x y")


def xy_dist(a, b):
    return math.sqrt((a.x - b.x) ** 2 + ((a.y) - b.y) ** 2)

class PosXYZ:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, value):
            self._x = value

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, value):
            self._y = value

        @property
        def z(self):
            return self._z

        @z.setter
        def z(self, value):
            self._z = value

# Position Class:
# Values are stored in decimal, in floating-point attributes
# (Python's float is a double-precision C++)
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
                raise ValueError(
                    "Latitude value must be between -90.0 and +90.0 degrees"
                )
            else:
                self._lat = value

        @property
        def long(self):
            return self._long

        @long.setter
        def long(self, value):
            if (value < -180.0) or (value > 180.0):
                raise ValueError(
                    "Longitude value must be between -180.0 and +180.0 degrees"
                )
            else:
                self._long = value

        @property
        def alt(self):
            return self._alt

        @alt.setter
        def alt(self, value):
            self._alt = value

    def __str__(self):
        return (
            "Lat="
            + str(self.lat)
            + "; Long="
            + str(self.long)
            + "; Alt="
            + str(self.alt)
        )

    def to_xy(self):
        x = EARTH_RADIUS * math.radians(self.long) * math.cos(math.radians(self.lat))
        y = EARTH_RADIUS * math.radians(self.lat)
        return XYPoint(x, y)

    def to_PosXYZ(self):
        xy = self.to_xy()
        return PosXYZ(xy.x, xy.y, self.alt)

    # φ: Latitude
    # λ: Longitude
    # x = r λ cos(φ0)
    # y = r φ
    def __eq__(self, pos):
        return (
            math.isclose(self.lat, pos.lat, abs_tol=ABSOLUTE_LAT_TOLERANCE)
            and math.isclose(self.long, pos.long, abs_tol=ABSOLUTE_LAT_TOLERANCE)
            and math.isclose(self.alt, pos.alt, abs_tol=ABSOLUTE_ALT_TOLERANCE)
        )
