// Includes functions for fetching and displaying weather alert information.
// For now, locations will be hardcoded in for Cleveland.

// Alert type code reference
// http://www.wunderground.com/weather/api/d/docs?d=data/alerts
// ^(\w+) 	(.+)$
// '\1': '\2',
var alertCodeLookup = {
	'HUR': 'Hurricane Local Statement',
	'TOR': 'Tornado Warning',
	'TOW': 'Tornado Watch',
	'WRN': 'Severe Thunderstorm Warning',
	'SEW': 'Severe Thunderstorm Watch',
	'WIN': 'Winter Weather Advisory',
	'FLO': 'Flood Warning',
	'WAT': 'Flood Watch / Statement',
	'WND': 'High Wind Advisory',
	'SVR': 'Severe Weather Statement',
	'HEA': 'Heat Advisory',
	'FOG': 'Dense Fog Advisory',
	'SPE': 'Special Weather Statement',
	'FIR': 'Fire Weather Advisory',
	'VOL': 'Volcanic Activity Statement',
	'HWW': 'Hurricane Wind Warning',
	'REC': 'Record Set',
	'REP': 'Public Reports',
	'PUB': 'Public Information Statement'
};

function severeWeatherAlert(){
	// Load the alerts information file.
	$.getJSON('info.json', function(data){
		if (data != ""){
			if (!document.getElementById("alertInformation")){
				$("#alertBanner").append('<div id="alertInformation">Alert</div>');
			}
		} else {
			$("#alertBanner").empty();
		}
	});
	/*
	.done(function(){ console.log("success"); })
	.fail(function(){ console.log("error"); })
	.always(function(){ console.log("complete"); });
	*/
}

function loadAlerts(){
}
