function loadPlotData() {
    var dateKeyName = 'DATA_DATE';
    var times = dfData_g[dateKeyName];
    // create traces array
    traces = [];
    dataKeys = Object.keys(dfData_g);
    for (let measIter = 0; measIter < dataKeys.length; measIter++) {
        var meas = dataKeys[measIter];
        if (meas == dateKeyName) {
            continue;
        }
        var trace = {
            x: times,
            y: dfData_g[meas],
            mode: 'lines+markers',
            name: meas
        };
        traces.push(trace);
    }
    var layout = {
        showlegend: true,
        legend: { "orientation": "h" }
    };
    Plotly.newPlot('pmuDiv', traces, layout);
}