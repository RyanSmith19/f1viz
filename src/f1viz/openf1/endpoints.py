from enum import StrEnum


class OpenF1Endpoint(StrEnum):
    CAR_DATA = "car_data"
    DRIVERS = "drivers"
    INTERVALS = "intervals"
    LAPS = "laps"
    LOCATION = "location"
    MEETINGS = "meetings"
    OVERTAKES = "overtakes"
    PIT = "pit"
    POSITION = "position"
    RACE_CONTROL = "race_control"
    SESSIONS = "sessions"
    STINTS = "stints"
    TEAM_RADIO = "team_radio"
    WEATHER = "weather"

