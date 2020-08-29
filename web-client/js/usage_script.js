var data_per_days = {};
var active_chart = undefined;
var dataFromTheRequest = undefined;

$('#show-table').on('click', function(event) {
    hideAll();

    $('#overall-table').removeAttr('hidden');
    
});

$('#show-evolution').on('click', function(event) {
    hideAll();

    $('#option-show-evolution').removeAttr('hidden');
    
});

$('#show-raw-json').on('click', function(event) {
    hideAll();

    $('#raw-json').removeAttr('hidden');
});

$('#reload-button').on('click', function(event) {
    loadData();
    alert("Data has been reloaded!")
});

var showRawJson = function () {
    $("#raw-json-text-area").val(JSON.stringify(dataFromTheRequest, null, 2));
}

var hideAll = function() {
    $('#option-show-evolution').attr('hidden', true);
    $('#raw-json').attr('hidden', true);
    $('#overall-table').attr('hidden', true);
}

var updateDropdownMenu = function(labels) {
    for (label of labels) {
        var element = document.createElement("option");

        element.value = label;
        element.innerText = label;

        $("#day-selector").append(element);
    }
}

var updateTable = function() {
    $('#table-scroll').empty();

    for (current of dataFromTheRequest) {
        var date_and_time = current.datetime.split(' ')
        var row = $('<tr><td>' + date_and_time[0] + '</td><td>' + date_and_time[1] + '</td><td>' + current.meter_usage + '</td></tr>');
        $('#table-scroll').append(row);
    }
}

$('select').on('change', function(e){
    var value = this.value;

    if (active_chart !== undefined)
        active_chart.destroy()

    if (data_per_days[value] === undefined) {
        return;
    }
    
    var data_in_current_day = data_per_days[value]

    let values = data_in_current_day.map(x => x.usage)
    let labels = data_in_current_day.map(x => x.time)

    updateChart('usage-chart', 'rgba(100, 20, 200, 0.3)', 'Usage', values, labels)
    $('#usage-chart').show()
});

var loadData = function() {
    $.ajax({
        type: 'GET',
        crossDomain: true,
        contentType: 'application/json',
        url: 'http://localhost:5000/',
        success: function(data){
                hideAll();
                dataFromTheRequest = JSON.parse(data); 

                for (var current of dataFromTheRequest) {
                    var usage = current.meter_usage;
                    var datetime = current.datetime;

                    var tokens = datetime.split(' ');
                    var day = tokens[0];
                    var time = tokens[1];

                    if (data_per_days[day] == undefined)
                        data_per_days[day] = []

                    data_per_days[day].push({"time" : time, "usage": usage});
                }

                updateTable();
                updateDropdownMenu(Object.keys(data_per_days));
                showRawJson();
            }
        })
}


$(document).ready(loadData());

// https://www.chartjs.org/docs/latest/
var updateChart = function(chartId, backgroudColor, label, data, labels) {
    var ctx = document.getElementById(chartId).getContext('2d');
    active_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label:label,
                data: data,
                backgroundColor: backgroudColor,
                borderColor: 'rgba(200, 50, 100, 1)',
                borderWidth: 1
            }]
        }
    });
}