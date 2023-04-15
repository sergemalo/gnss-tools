import re
from datetime import datetime, timezone

# https://docs.novatel.com/OEM7/Content/Logs/GPRMC.htm
# Example:
# $GPRMC,203522.00,A,5109.0262308,N,11401.8407342,W,0.004,133.4,130522,0.0,E,D*2B


class RMCSentence:
    def __init__(self):
        self.utc_datetime = datetime(
            1980, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc
        )


def parse_GPRMC(in_sentence: str):
    fields = re.split(r"\,", in_sentence)
    if fields and fields[0][3:6] != "RMC":
        raise TypeError("Sentence is not NMEA XXRMC")

    result = RMCSentence()

    utc_time = re.match(r"\s*(\d{2})(\d{2})(\d{2})(\.*)(\d*)\s*", fields[1])
    if utc_time is None:
        raise RuntimeError("Unable to parse UTC Time")
    hours = int(utc_time.group(1))
    minutes = int(utc_time.group(2))
    seconds = int(utc_time.group(3))
    m_secs = 0
    if utc_time.group(5):
        m_secs = int(
            (float(utc_time.group(5)) / (10 ** len(utc_time.group(5)))) * 1000000
        )

    utc_date = re.match(r"\s*(\d{2})(\d{2})(\d{2})\s*", fields[9])
    if utc_date is None:
        raise RuntimeError("Unable to parse UTC Date")
    day = int(utc_date.group(1))
    month = int(utc_date.group(2))
    year = int(utc_date.group(3))
    if year < 80:
        year = year + 2000
    else:
        year = year + 1900

    result.utc_datetime = datetime(
        year, month, day, hours, minutes, seconds, m_secs, tzinfo=timezone.utc
    )
    return result
