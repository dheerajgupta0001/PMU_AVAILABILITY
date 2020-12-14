from typing import TypedDict
import datetime as dt


class IPmuAvailabilityReportSummary(TypedDict):
    pmu_location: str
    avg_availability_perc: float
    days_count: int
