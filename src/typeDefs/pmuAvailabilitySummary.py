from typing import TypedDict
import datetime as dt


class IPmuAvailabilitySummary(TypedDict):
    DATA_DATE: dt.datetime
    PMU_LOCATION: str
    AVAILABILITY_PERC: float
    DATA_VALID_PERC:float
    DATA_ERROR_PERC:float
    GPS_LOCKED_PERC:float

