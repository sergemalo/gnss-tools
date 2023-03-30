from nmea import toto
from nmea import talker_id
from nmea import msg_type
from position import Position
from gga import parse_GPGGA
from rmc import parse_GPRMC
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


def unit_test_GPGGA(sentence, expectedTime, expectedPos):
    parsedPos = Position()

    print(sentence)

    parsedGPGGA = parse_GPGGA(sentence)
    parsedPos.lat = parsedGPGGA.lat
    parsedPos.long = parsedGPGGA.long
    parsedPos.alt = parsedGPGGA.alt

    if not math.isclose(parsedGPGGA.utcTime, expectedTime, abs_tol=0.0000000001):
        print("Invalid UTC Time")
        print("Expected: " + str(expectedTime))
        print("Parsed  : " + str(parsedGPGGA.utcTime))
        return False
    if expectedPos != (parsedPos):
        print("Invalid Position")
        print("Expected: " + str(expectedPos))
        print("Parsed  : " + str(parsedPos))
        return False
    return True


def test_gpgga():

    expectedPos = Position(-43.1234, -73.0, 2.0)
    assert unit_test_GPGGA(
        "$GPGGA,120000.000,4307.4040,S,07300.0000,W,1,9,0.91,2.0,M,,M,,*55",
        12 * 3600.0,
        expectedPos,
    )
    expectedPos = Position(37.387458333, -121.97236, 9.0)
    assert unit_test_GPGGA(
        "$GPGGA, 161229.487, 3723.2475, N, 12158.3416, W, 1, 07, 1.0, 9.0, M, , , , 0000*18",
        16 * 3600.0 + 12 * 60.0 + 29.487,
        expectedPos,
    )
    expectedPos = Position(33.5705224283, -112.1842949, 354.682)
    assert unit_test_GPGGA(
        "$GPGGA,001038.00,3334.2313457,N,11211.0576940,W,2,04,5.4,354.682,M,- 26.574,M,7.0,0138*79",
        10 * 60.0 + 38.0,
        expectedPos,
    )

def test_gprmc():
    expected = datetime(1995, 4, 13, 21, 2, 30, tzinfo=timezone.utc)
    test_val = parse_GPRMC(
        "$GPRMC,210230,A,3855.4487,N,09446.0071,W,0.0,076.2,130495,003.8,E*69")
    assert(test_val.utc_datetime == expected)
    expected = datetime(2022, 5, 13, 20, 35, 22, 120000, tzinfo=timezone.utc)
    test_val = parse_GPRMC(
        "$GPRMC,203522.12,A,5109.0262308,N,11401.8407342,W,0.004,133.4,130522,0.0,E,D*2B")
    assert(test_val.utc_datetime == expected)


def test_lla_to_xy():
    pos = Position(0, 0, 0)
    expected = (0.0, 0.0)
    assert(expected == pos.to_xy())
    pos = Position(0, 1, 0)
    expected = (111195.080, 0.0)
    assert(expected == pos.to_xy())
    pos = Position(1, 0, 0)
    expected = (0.0, 111195.080)
    assert(expected == pos.to_xy())

