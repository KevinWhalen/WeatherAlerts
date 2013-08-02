// Includes functions for fetching and displaying weather alert information.
// For now, locations will be hardcoded in for Cleveland.


// Remove once record['location'] is implemented.
loc = "Ohio";


// Turns the alert banner on or off.
function severeWeatherAlert(){
	// Load the alerts information file.
	$.getJSON('info.json', function(data){
		if (data != ""){
			if ($("#alertBanner").is(':hidden')){
				$("#alertBanner").slideDown();
			}
			if (document.getElementById("minimizeAlertInformation")){
				clearAlerts();
				appendAlertInformation(data);
			}
			displayAlertHeader(data);
		}
	}).fail(function(){
		// Reset the alert banner
		$("#alertBanner").hide();
		$("#alertBanner").off('click');
		$("#alertBanner").empty();
	});
}


function displayAlertHeader(data){
	var header = "<h3>Severe Weather Alert</h3>";
	if (!document.getElementById("alertHeader")){
		$('#alertBanner')
			.append('<div id="alertHeader">' + header + '</div>')
			.append('<div id="expandAlertHeader">[Click To Expand]</div>');
		$('#alertBanner')
			.click(function(){
				$('#expandAlertHeader').hide();
				appendAlertInformation(data);
			});
	}
}


function appendAlertInformation(details){
	if (document.getElementById("minimizeAlertInformation")){
		clearAlerts();
	}
	var alertInfo = "";
	$.each(details, function(idx, record){
		alertInfo = "<h4>" + loc /*record['location']*/ + " - " 
			+ record['description'] + " - Until: " + record['expires'] 
			+ "</h4>" + "<p>Starting at " + record['date'] 
			+ " : <br />" + record['message'] + "</p><p>Type: " 
			+ record['type'] + " | Phenomena: " + record['phenomena'] 
			+ " | Significance: " + record['significance'] + "</p>";
		$('#alertBanner')
			.append('<div class="alertInformation">' + alertInfo + '</div>')
			.slideDown(400, function(){
				$('#alertBanner').append('<hr class="alertDivider" />')
			});
	});
	/* Minimum image size allowed by Weather Underground is 126px */
	$('#alertBanner')
		.append('<div id="minimizeAlertInformation"><div '
		+ 'id="alertFooter">For more information go to '
		+ '<a href="http://www.wunderground.com/severe.asp?'
		+ 'apiref=b7583f58544ad7f7" target="_blank">'
		+ '<img width="150px" alt="Weather Underground" '
		+ 'title="US Severe Weather Map" src="'
		+ 'http://icons.wxug.com/logos/PNG/wundergroundLogo_4c_horz.png" '
		+ '/></a></div>[Click To Hide]</div>')
		.click(function(){
			$('#alertBanner').empty();
			//clearAlerts();

			// Clear click event handlers from banner
			$("#alertBanner").off('click');

			$('#expandAlertHeader').show();
			severeWeatherAlert();
		})
		.slideDown();
}


function clearAlerts(){
	$('.alertInformation').remove();
	$('.alertDivider').remove();
	$('#minimizeAlertInformation').remove();
}



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
