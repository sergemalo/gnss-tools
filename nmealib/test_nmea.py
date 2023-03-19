from nmea import Position, parse_GPGGA
import math

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
