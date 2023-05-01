from nmea import toto
from nmea import talker_id
from nmea import msg_type
from position import PosLLA, XYPoint, xy_dist, PosXYZ
from gga import parse_GGA
from rmc import parse_RMC
from rmc import RMCSentence
import math
from datetime import datetime, timezone


def test_toto():
    toto()


def test_talker_id():
    tid = talker_id(
        """$GNRMC,141504.00,A,4533.04027,N,07336.12353,W,0.004,,140323,,,A,V*07"""
    )
    assert tid == "GN"
    tid = talker_id("$GNVTG,,T,,M,0.004,N,0.007,K,A*3E")
    assert tid == "GN"
    tid = talker_id(
        "$GNGGA,141504.00,4533.04027,N,07336.12353,W,1,12,0.49,62.9,M,-32.6,M,,*4B"
    )
    assert tid == "GN"


def test_msg_type():
    msg_t = msg_type(
        "$GNRMC,141504.00,A,4533.04027,N,07336.12353,W,0.004,,140323,,,A,V*07"
    )
    assert msg_t == "RMC"
    msg_t = msg_type("$GNVTG,,T,,M,0.004,N,0.007,K,A*3E")
    assert msg_t == "VTG"
    msg_t = msg_type(
        "$GNGGA,141504.00,4533.04027,N,07336.12353,W,1,12,0.49,62.9,M,-32.6,M,,*4B"
    )
    assert msg_t == "GGA"


def unit_test_GGA(sentence, expectedTime, expectedPos):
    parsedPos = PosLLA()

    print(sentence)

    parsedGGA = parse_GGA(sentence)
    parsedPos.lat = parsedGGA.lat
    parsedPos.long = parsedGGA.long
    parsedPos.alt = parsedGGA.alt

    if not math.isclose(parsedGGA.utcTime, expectedTime, abs_tol=0.0000000001):
        print("Invalid UTC Time")
        print("Expected: " + str(expectedTime))
        print("Parsed  : " + str(parsedGGA.utcTime))
        return False
    if expectedPos != (parsedPos):
        print("Invalid PosLLA")
        print("Expected: " + str(expectedPos))
        print("Parsed  : " + str(parsedPos))
        return False
    return True


def test_gga():

    expectedPos = PosLLA(-43.1234, -73.0, 2.0)
    assert unit_test_GGA(
        "$GPGGA,120000.000,4307.4040,S,07300.0000,W,1,9,0.91,2.0,M,,M,,*55",
        12 * 3600.0,
        expectedPos,
    )
    expectedPos = PosLLA(37.387458333, -121.97236, 9.0)
    assert unit_test_GGA(
        "$GPGGA, 161229.487, 3723.2475, N, 12158.3416, W, 1, 07, 1.0, 9.0, M, , , , 0000*18",
        16 * 3600.0 + 12 * 60.0 + 29.487,
        expectedPos,
    )
    expectedPos = PosLLA(33.5705224283, -112.1842949, 354.682)
    assert unit_test_GGA(
        "$GPGGA,001038.00,3334.2313457,N,11211.0576940,W,2,04,5.4,354.682,M,- 26.574,M,7.0,0138*79",
        10 * 60.0 + 38.0,
        expectedPos,
    )

    expectedPos = PosLLA(45.55067116666667, -73.60205883333333, 62.9)
    assert unit_test_GGA(
        "$GNGGA,141505.00,4533.04027,N,07336.12353,W,1,12,0.49,62.9,M,-32.6,M,,*4A",
        14 * 3600 + 15 * 60.0 + 5.0,
        expectedPos,
    )

    expectedPos = PosLLA(45.55067116666667, -73.60205866666666, 62.9)
    assert unit_test_GGA(
        "$GNGGA,141506.00,4533.04027,N,07336.12352,W,1,12,0.49,62.9,M,-32.6,M,,*48",
        14 * 3600 + 15 * 60.0 + 6.0,
        expectedPos,
    )


def test_rmc():
    expected = datetime(1995, 4, 13, 21, 2, 30, tzinfo=timezone.utc)
    test_val = parse_RMC(
        "$GPRMC,210230,A,3855.4487,N,09446.0071,W,0.0,076.2,130495,003.8,E*69")
    assert(test_val.utc_datetime == expected)
    expected = datetime(2022, 5, 13, 20, 35, 22, 120000, tzinfo=timezone.utc)
    test_val = parse_RMC(
        "$GPRMC,203522.12,A,5109.0262308,N,11401.8407342,W,0.004,133.4,130522,0.0,E,D*2B")
    assert(test_val.utc_datetime == expected)


def test_lla_to_xy():
    my_abs_tol = 0.001 # 1mm absolute totelance

    pos = PosLLA(0, 0, 0)
    expectedXY = XYPoint(0.0, 0.0)
    testXY = pos.to_xy()
    assert(math.isclose(expectedXY.x, testXY.x, abs_tol = my_abs_tol) and
           math.isclose(expectedXY.y, testXY.y, abs_tol = my_abs_tol))

    pos = PosLLA(0, 1, 0)
    expectedXY = XYPoint(111195.080, 0.0)
    testXY = pos.to_xy()
    assert(math.isclose(expectedXY.x, testXY.x, abs_tol = my_abs_tol) and
           math.isclose(expectedXY.y, testXY.y, abs_tol = my_abs_tol))

    pos = PosLLA(1, 0, 0)
    expectedXY = XYPoint(0.0, 111195.080)
    testXY = pos.to_xy()
    assert(math.isclose(expectedXY.x, testXY.x, abs_tol = my_abs_tol) and
           math.isclose(expectedXY.y, testXY.y, abs_tol = my_abs_tol))

def test_dist_xy():
    a = XYPoint(x=0, y=0)
    b = XYPoint(x=1, y=0)
    assert(xy_dist(a, b) == 1.0)
    b = XYPoint(x=1, y=1.0)
    assert(xy_dist(a, b) == math.sqrt(2))



def test_lla_to_PosXYZ():
    my_abs_tol = 0.001 # 1mm absolute totelance

    pos = PosLLA(0, 0, 0)
    expectedPosXYZ = PosXYZ(0.0, 0.0, 0.0)
    testXYZ = pos.to_PosXYZ()
    assert(math.isclose(expectedPosXYZ.x, testXYZ.x, abs_tol = my_abs_tol) and
           math.isclose(expectedPosXYZ.y, testXYZ.y, abs_tol = my_abs_tol) and
           math.isclose(expectedPosXYZ.z, testXYZ.z, abs_tol = my_abs_tol))


    pos = PosLLA(0, 0, 1234.56)
    expectedPosXYZ = PosXYZ(0.0, 0.0, 1234.56)
    testXYZ = pos.to_PosXYZ()
    assert(math.isclose(expectedPosXYZ.x, testXYZ.x, abs_tol = my_abs_tol) and
           math.isclose(expectedPosXYZ.y, testXYZ.y, abs_tol = my_abs_tol) and
           math.isclose(expectedPosXYZ.z, testXYZ.z, abs_tol = my_abs_tol))

