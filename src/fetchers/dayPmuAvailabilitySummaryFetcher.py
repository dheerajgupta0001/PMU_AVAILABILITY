import datetime as dt
from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary
from typing import List
import os
import pandas as pd
import cx_Oracle


def fetchPmuAvailabilitySummaryForDate(pmuFolderPath: str, targetDt: dt.datetime) -> List[IPmuAvailabilitySummary]:
    """fetched pmu availability summary data rows for a date from excel file

    Args:
        targetDt (dt.datetime): date for which data is to be extracted

    Returns:
        List[IPmuAvailabilitySummary]: list of pmu availability records fetched from the excel data
    """
    # sample excel filename - PMU_availability_Report_05_08_2020.xlsx
    fileDateStr = dt.datetime.strftime(targetDt, '%d_%m_%Y')
    targetFilename = 'PMU_availability_Report_{0}.xlsx'.format(fileDateStr)
    targetFilePath = os.path.join(pmuFolderPath, targetFilename)

    # check if excel file is present
    if not os.path.isfile(targetFilePath):
        print("Excel file for date {0} is not present".format(targetDt))
        return []

    # read pmu excel 
    excelDf = pd.read_excel(targetFilePath, 'MAIN_REPORT', skiprows=8)
    
    # remove first and second column from df
    excelDf = excelDf.iloc[:, 2:7]
    excelDf.loc[:,'Availability %'] *= 100
    excelDf.loc[:,'Data Valid (%)'] *= 100
    excelDf.loc[:,'Data Error (%)'] *= 100
    excelDf.loc[:,'GPS Locked (%)'] *= 100
    excelDf['DATA_DATE'] = targetDt
    excelDf.rename({'PMU Location':'PMU_LOCATION',
            'Availability %':'AVAILABILITY_PERC', 'Data Valid (%)':'DATA_VALID_PERC',
            'Data Error (%)':'DATA_ERROR_PERC', 'GPS Locked (%)':'GPS_LOCKED_PERC'}, axis=1, inplace =True)
    # drop duplicates and keep last value if same duplicates
    excelDf = excelDf.drop_duplicates(
        subset=['PMU_LOCATION', 'DATA_DATE'], keep='last', ignore_index=True)

    # convert nan to None
    excelDf = excelDf.where(pd.notnull(excelDf), None)

    # convert dataframe to list of dictionaries
    resRecords = excelDf.to_dict('records')
    #print(resRecords)
    
    return resRecords
