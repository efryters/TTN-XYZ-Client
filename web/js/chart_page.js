// Eric Fryters
// Charting client

// Create globals for charting
var sensor_data_array = new Array();
var dates_array = new Array();
var temperature_array = new Array();
var moisture_array = new Array();
var light_array = new Array();
var ctx = document.getElementById('myChart').getContext('2d');

// Create HTTP client
var xhr = new XMLHttpRequest();


// Run when chart.html loads
var loaded = function () {
    console.log("Loaded page");

    let param_type = getParameterByName('type');

    if (param_type == "latest") {
        let api_obj = {
            "type": param_type
        };
        xhr.open('GET', `./get_data?type=${api_obj.type}`, true);
    } else if (param_type == "ranged") {
        let time_from = getParameterByName('from');
        let time_to = getParameterByName('to');

        let api_obj = {
            "type": param_type,
            "from": time_from,
            "to": time_to
        };
        xhr.open('GET', `./get_data?type=${api_obj.type}&time_from=${api_obj.from}&time_to=${api_obj.to}`, true);
    } else {
        return null;
    }

    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);
    console.log("XHR listener added");

    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            console.log("XHR request 4");
            var response = JSON.parse(xhr.responseText);
            response.forEach(row => {
                sensor_data_array.push(row[0]);
                light_array.push(row[2]);
                temperature_array.push(row[3]);
                moisture_array.push(row[4]);
            });
            // Convert epoch dates to readable dates
            sensor_data_array.forEach(epoch_date => {
                let date = new Date(epoch_date * 1000);

                var date_str = date.toLocaleString();
                dates_array.push(date_str);
            });
            data_to_chart = [dates_array, light_array, temperature_array, moisture_array];
            make_chart(data_to_chart);
        }
    };
}

var get_data_request = (xhr_req) => {

}

var periodic_update = (timer) => {

}

var make_chart = (data_arr) => {
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data_arr[0],
            datasets: [{
                    data: data_arr[1],
                    label: "Light",
                    fill: false,
                    borderColor: "#CCCC00",
                    yAxisID: "others"
                },
                {
                    data: data_arr[2],
                    label: "Temperature",
                    fill: false,
                    borderColor: "#FF6666",
                    yAxisID: "temp"
                },
                {
                    data: data_arr[3],
                    label: "Moisture",
                    fill: false,
                    borderColor: "#0080FF",
                    yAxisID: "others"
                }
            ]
        },

        options: {
            scales: {
                yAxes: [
                    {
                    id: "temp",
                    type: "linear",
                    position: "right",
                    ticks: {
                        min: -20,
                        max: 80
                    }
                    },
                    {
                        id      : "others",
                        type    : "linear",
                        position: "left"
                    }
            ]
            }
        }
    })
};

/*
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Red'],
                datasets: [{
                    label: '# of Votes',
                    data: [1,2,3,4,5],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
        */

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}