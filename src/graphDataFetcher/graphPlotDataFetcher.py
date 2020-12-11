from typing import List, Tuple, TypedDict
import cx_Oracle
import datetime as dt
import os
import pandas as pd
from flask import Flask, request, jsonify, render_template

class PlotPmuAvailabilityData():
    """Repository class for pmu availability summary data
    """
    localConStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConf (DbConfig): database connection string
        """
        self.localConStr = dbConStr
# lis=[]
    def plotPmuAvailabilityData(self, startDate: dt.datetime, endDate: dt.datetime, pmuList: [], colData: str):
        """fetchess pmu availability data from the app db
        Args:
            appDbConStr (str): application db connection string
            pmuList (List): List of PMU Location for graph plot
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            dictionary of lists of pmu availability data!!!
        """
        try:
            connection = cx_Oracle.connect(self.localConStr)
            cursor = connection.cursor()
            sql_fetch = f""" 
                        select data_date, pmu_location, {colData}
                        from mis_warehouse.pmu_availability
                        where
                        data_date between to_date(:start_date) and to_date(:end_date)
                        and pmu_location in {tuple(pmuList)}
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            data = pd.read_sql(sql_fetch, params={
                'start_date': startDate, 'end_date': endDate}, con=connection)
            data= data.pivot_table(index=["DATA_DATE"],
                                    columns='PMU_LOCATION', values=colData).reset_index()
            print(type(data['DATA_DATE']))
            dateList = []
            for col in data['DATA_DATE']:
                dateList.append(dt.datetime.strftime(col, '%Y-%m-%d'))
            data['DATA_DATE'] = dateList
        except Exception as e:
            print('Error while fetching pmu availability data from db')
            print(e)
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after pmu availability data fetching')
        
        # convert dataframe to list of dictionaries
        resRecords = data.to_dict(orient='list')
        #print(resRecords)

        return resRecords