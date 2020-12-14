from typing import List, Tuple, TypedDict
import cx_Oracle
import datetime as dt
import os
import pandas as pd
from src.typeDefs.pmuAvailabilityReportSummary import IPmuAvailabilityReportSummary

class FetchPmuAvailabilityData():
    """Repository class for pmu availability summary data
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr

    def fetchPmuAvailabilityData(self, startDate: dt.datetime, endDate: dt.datetime ) -> pd.core.frame.DataFrame:
        """fetchess pmu availability data from the app db
        Args:
            appDbConStr (str): application db connection string
            pmuFolderPath (str): folder path of pmu availability data excel files
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            bool: pmu availability data fetching is successful or not!!!
        """
        try:
            connection = cx_Oracle.connect(self.localConStr)
            cursor = connection.cursor()
            sql_fetch = """ 
                        select pmu_location, AVG(availability_perc), COUNT(availability_perc)
                        from mis_warehouse.pmu_availability
                        where
                        data_date between to_date(:start_date) and to_date(:end_date)
                        group by pmu_location
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            data = pd.read_sql(sql_fetch, params={
                'start_date': startDate, 'end_date': endDate}, con=connection)
        except Exception as e:
            print('Error while fetching pmu availability data from db')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after pmu availability data fetching')
        return data
    def createAverageReport(self, dumpFolder: str, startDate: dt.datetime, endDate: dt.datetime, data) -> bool:
        isInsertSuccess = False
        if len(data)>0:
            isInsertSuccess = True
        data['AVG(AVAILABILITY_PERC)'] = data['AVG(AVAILABILITY_PERC)'].round(decimals= 4)
        # generate file name
        dumpFileName = 'PMU_availability_Report_average_{0}_to_{1}.csv'.format(dt.datetime.strftime(
            startDate, '%d-%m-%Y'), dt.datetime.strftime(endDate, '%d-%m-%Y'))
        dumpFileFullPath = os.path.join(dumpFolder, dumpFileName)
        data.to_csv(dumpFileFullPath, index=False)

        return isInsertSuccess

    def createPmuAvailabilityList(self, startDate: dt.datetime, endDate: dt.datetime, df) -> List[IPmuAvailabilityReportSummary]:
        pmuAvailabilityList: List[IPmuAvailabilityReportSummary] = []
        df['AVG(AVAILABILITY_PERC)'] = df['AVG(AVAILABILITY_PERC)'].round(decimals= 4)
        for i in df.index:
            pmuAvail: IPmuAvailabilityReportSummary = {
                'pmu_location': df['PMU_LOCATION'][i],
                'avg_availability_perc': df['AVG(AVAILABILITY_PERC)'][i],
                'days_count': df['COUNT(AVAILABILITY_PERC)'][i],
            }
            pmuAvailabilityList.append(pmuAvail)
        return pmuAvailabilityList