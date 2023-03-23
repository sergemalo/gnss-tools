
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

