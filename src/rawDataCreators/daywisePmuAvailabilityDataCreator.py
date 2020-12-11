from src.fetchers.dayPmuAvailabilitySummaryFetcher import fetchPmuAvailabilitySummaryForDate
import datetime as dt
import cx_Oracle
from typing import List
from src.repos.dailyPmuAvailabilityDataRepo import DailyPmuAvailabilityDataRepo


def createPmuAvailabilityRawData(appDbConStr: str, pmuFolderPath: str, startDate: dt.datetime, endDate: dt.datetime) -> bool:
    """fetches the pmu availability data from excel files 
    and pushes it to the raw data table
    Args:
        appDbConStr (str): application db connection string
        pmuFolderPath (str): folder path of pmu availability data excel files
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
    Returns:
        [bool]: returns True if succeded
    """
    isRawDataInsSuccess = False

    reqStartDt = startDate.date()
    reqEndDt = endDate.date()

    if reqEndDt < reqStartDt:
        return False

    #get the instance of pmu availability repository
    pmuDataRepo = DailyPmuAvailabilityDataRepo(appDbConStr)
    currDate = reqStartDt

    while currDate <= reqEndDt:
        # fetch pmu data
        pmuAvailabilityData = fetchPmuAvailabilitySummaryForDate(pmuFolderPath, currDate)

        # insert pmu availability data into db via the repository instance
        isRawDataInsSuccess = pmuDataRepo.insertPmuAvailabilityData(pmuAvailabilityData)

        if isRawDataInsSuccess:
            print("Pmu Availability Data creation for date {} is SUCCESSFUL".format(currDate))
        else:
            print("Pmu Availability Data creation for date {} is UNSUCCESSFUL".format(currDate))

        # update currDate
        currDate += dt.timedelta(days=1)

    return isRawDataInsSuccess
