var loaded = function() {
    console.log("Loaded page");

    let param_type = getParameterByName('type');
    
    if (param_type == "latest") {
        let api_obj = {
            "type" : param_type
        }
    }
    else if (param_type == "ranged") {
        let time_from   = getParameterByName('from');
        let time_to     = getParameterByName('to');

        let api_obj = {
            "type" : param_type,
            "from" : time_from,
            "to"   : time_to
        }
    }

    


}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
