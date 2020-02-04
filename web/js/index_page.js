//Eric Fryters
//Index page handler

var xhr = new XMLHttpRequest();

var loaded = function () {
    
    xhr.open('GET', './get_unique_devices')
    xhr.send();
    xhr.addEventListener("readystatechange", processRequest, false);


    function processRequest(e) {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var selectBlock = $("#devices");    // Select the listbox element

            var response = JSON.parse(xhr.responseText);
            response.forEach(item => {
                var opt = document.createElement("option");
                opt.value = item;
                opt.innerHTML = item;
                selectBlock.append(opt);
            });
        }
    }
}


var btn_latest_click = () =>
{
    var selectedDevice = $("#devices option:selected").val();    
    location.replace(`./chart.html?type=latest&device_id=${selectedDevice}`)
}

var btn_ranged_click = () =>
{
    var date_from = $("#datetimepicker6").children()[0];
    var date_to = $("#datetimepicker7").children()[0];
    var selectedDevice = $("#devices option:selected").val();
    
    var epoch_from, epoch_to = 0;

    if (date_from.value != "" || date_to.value != "")
    {
        epoch_from = (new Date(date_from.value).valueOf()) / 1000;
        epoch_to = (new Date(date_to.value).valueOf()) / 1000;
    }
    else
    {
        alert("Date boxes cannot be empty.")
    }

    if(epoch_from != 0 || epoch_to != 0)
    {
        location.replace(`./chart.html?type=ranged&from=${epoch_from.toString()}&to=${epoch_to.toString()}&device_id=${selectedDevice}`);
    }
}