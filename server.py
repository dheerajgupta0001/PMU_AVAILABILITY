'''
This is the web server that acts as a service that creates outages raw data
'''
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
from flask import Flask, request, jsonify, render_template
import datetime as dt
import pandas as pd
import json
import os
from waitress import serve
from src.config.appConfig import getConfig
from src.rawDataCreators.daywisePmuAvailabilityDataCreator import createPmuAvailabilityRawData
from src.averageDataFetcher.pmuDataFetcher import FetchPmuAvailabilityData
from src.graphDataFetcher.graphPlotDataFetcher import PlotPmuAvailabilityData

app = Flask(__name__)

# get application config
appConfig = getConfig()

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# create pmu availability raw data between start and end dates
pmuFolderPath = appConfig['pmuFolderPath']
appDbConnStr = appConfig['appDbConStr']
dumpFolder = appConfig['dumpFolder']

@app.route('/')
def hello():
    return render_template('home.html.j2')


@app.route('/createPmuAvailabilityData', methods=['GET', 'POST'])
def createPmuAvailabilityData():
    # in case of post request, create Pmu Availability Data and return reponse
    if request.method == 'POST':
        try:
            startDate = request.form.get('startDate')
            endDate = request.form.get('endDate')
            startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
            endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
            print(startDate)
            isRawCreationSuccess = createPmuAvailabilityRawData(
                    appDbConnStr, pmuFolderPath, startDate, endDate)
            startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
            endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
            if isRawCreationSuccess:
                x=  {'message': 'Pmu Availability Data insertion successful!!!'}
                return render_template('createPmuAvailabilityData.html.j2', data= x, startDate= startDate, endDate= endDate)
        except Exception as ex:
            print(ex)
            x = jsonify({'message': 'some error occured...'}), 400
            return render_template('createPmuAvailabilityData.html.j2', data=x)

        return jsonify({'message': 'some error occured...'}), 400

    # in case of get request just return the html template
    return render_template('createPmuAvailabilityData.html.j2')

@app.route('/plotGraphPmuData', methods=['GET', 'POST'])
def plotGraphPmuData():
    # in case of post request, fetch iegc viol msgs and return json response
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')
        multiSelectList = request.form.getlist('pmu')
        colAttribute = request.form.get('col')
        print(multiSelectList)

        #get the instance of pmu availability repository for GRAPH PLOTTING
        plotPmuDataRepo = PlotPmuAvailabilityData(appDbConnStr)

        # insert pmu availability data into db via the repository instance
        dfData_g = plotPmuDataRepo.plotPmuAvailabilityData(startDate, endDate, multiSelectList, colAttribute)
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        return render_template('testGraph.html.j2', data= dfData_g, startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('testGraph.html.j2')

@app.route('/displayPmuAvailabilityData', methods=['GET', 'POST'])
def displayPmuAvailabilityData():
    # in case of post request, fetch iegc viol msgs and return json response
    if request.method == 'POST':
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        startDate = dt.datetime.strptime(startDate, '%Y-%m-%d')
        endDate = dt.datetime.strptime(endDate, '%Y-%m-%d')

        #get the instance of pmu availability repository for data fetching
        fetchPmuDataRepo = FetchPmuAvailabilityData(appDbConnStr)

        # insert pmu availability data into db via the repository instance
        avgData = fetchPmuDataRepo.fetchPmuAvailabilityData(startDate, endDate)

        # create pmu availability list for report
        data = fetchPmuDataRepo.createPmuAvailabilityList(startDate, endDate, avgData)
        startDate=dt.datetime.strftime(startDate, '%Y-%m-%d')
        endDate=dt.datetime.strftime(endDate, '%Y-%m-%d')
        return render_template('displayPmuAvailabilityData.html.j2', data= data, startDate= startDate, endDate= endDate)
    # in case of get request just return the html template
    return render_template('displayPmuAvailabilityData.html.j2')


if __name__ == '__main__':
    app.run(port=int(appConfig['flaskPort']), debug=True)
    ''''serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        app.run(host="0.0.0.0", port=int(appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(appConfig['flaskPort']), threads=1)'''
