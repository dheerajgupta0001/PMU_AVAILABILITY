from typing import List, Tuple, TypedDict
import cx_Oracle
from src.typeDefs.pmuAvailabilitySummary import IPmuAvailabilitySummary


class DailyPmuAvailabilityDataRepo():
    """Repository class for daywise pmu availability summary data
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr

    def insertPmuAvailabilityData(self, pmuDataRecords: List[IPmuAvailabilitySummary]) -> bool:
        """inserts pmu availability into the app db
        Args:
            pmuDataRecords (List[IPmuAvailabilitySummary]): daywise pmu availability data to be inserted
        Returns:
            bool: returns true if process is ok
        """
        # get connection with raw data table
        conLocal = cx_Oracle.connect(self.localConStr)

        isInsertSuccess = True
        if len(pmuDataRecords) == 0:
            return isInsertSuccess
        try:
            # keyNames names of the raw data
            keyNames = ['DATA_DATE', 'PMU_LOCATION', 'AVAILABILITY_PERC',
                        'DATA_VALID_PERC','DATA_ERROR_PERC','GPS_LOCKED_PERC']
            colNames = ['DATA_DATE', 'PMU_LOCATION', 'AVAILABILITY_PERC',
                        'DATA_VALID_PERC','DATA_ERROR_PERC','GPS_LOCKED_PERC']
            # get cursor for raw data table
            curLocal = conLocal.cursor()

            # text for sql place holders
            sqlPlceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(keyNames))])

            # delete the rows which are already present
            existingPmuAvailability = [(x['DATA_DATE'], x['PMU_LOCATION'])
                                  for x in pmuDataRecords]
            curLocal.executemany(
                "delete from mis_warehouse.PMU_AVAILABILITY where DATA_DATE=:1 and PMU_LOCATION=:2", existingPmuAvailability)

            # insert the raw data
            anglesDataInsSql = 'insert into mis_warehouse.PMU_AVAILABILITY({0}) values ({1})'.format(
                ','.join(colNames), sqlPlceHldrsTxt)

            curLocal.executemany(anglesDataInsSql, [tuple(
                [r[col] for col in keyNames]) for r in pmuDataRecords])

            # commit the changes
            conLocal.commit()
        except Exception as e:
            isInsertSuccess = False
            print('Error while bulk insertion of daily pmu availability data into raw data db')
            print(e)
        finally:
            # closing database cursor and connection
            if curLocal is not None:
                curLocal.close()
            conLocal.close()
        return isInsertSuccess
