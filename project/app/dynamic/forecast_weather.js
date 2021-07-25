// plot Chart

// Selecting the input element and get its value 
function plotChart(){
    // Get Input values from user
    var sensorId = document.getElementById("sensorId").value;
    var forecastTime =  document.getElementById("forecastTime").value;
    var trainTime = document.getElementById("trainTime").value;

    if (sensorId.length == 0) {sensorId = 'Temp-81'};
    if (forecastTime.length == 0) {forecastTime = 180};
    if (trainTime.length == 0) {trainTime = 3};

    url = '/forecast?sensorId=' + sensorId + '&trainTime=' + trainTime + '&forecastTime=' + forecastTime ;

    var data = JSON.parse(Get(url));
    console.log(data);

    labels = Object.values(data.data_dict.ds);
    console.log(labels);

    values =Object.values(data.data_dict.y);
    console.log(values);

    labels_forecast = Object.keys(data.forecastOut);
    console.log(labels_forecast);

    values_forecast =Object.values(data.forecastOut);
    console.log(values_forecast);

    BuildChart(labels, values, labels_forecast, values_forecast, 'Forecasting');

}

// build chart
function BuildChart(labels = [1, 2, 3], values = [3, 4, 5], labels_forecast = [4,5], values_forecast = [8,9], chartTitle) {
    var sensor_data = {
            x: labels,
            y: values,
            type: 'line + scatter',
            mode: 'lines + markers',
            name: 'Sensor Data'
    };

    var forecast = {
            x: labels_forecast,
            y: values_forecast,
            type: 'line + scatter',
            mode: 'lines + markers',
            name: 'Forecast'
    };

    data = [sensor_data, forecast];

    var layout = {
        title: 'Scroll and Zoom',
        plot_bgcolor:"#FFF3",
        paper_bgcolor:"#FFF3"
    };

    Plotly.newPlot("myChart", data, layout,  {scrollZoom: true}, {displaylogo: false}, {responsive: true});
}

// getting the data from api
function Post(Url){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("POST", Url, false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

// getting the data from api
function Get(Url){
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET", Url, false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}


