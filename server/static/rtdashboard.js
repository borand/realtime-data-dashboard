///////////////////////////////////////////
// Global variables
var debug_websocket = true;
var ws;
////////////////////////////////////////


/////////////////////////////////////////////////////////////////////
// UTILITY FUNCTIONS
//
//
function dbg(message, show) {	
	console.log(message);
}

function SendCmd(cmd, val) {
	return $.getJSON('/cmd/', "cmd=" + cmd + "&param=" + val, function(data) {			
		$("#cmd_status").text(data.cmd);
	});
}

///////////////////////////////////////////////////////////////////////
//

///////////////////////////////////////////////////////////////////////
// WEBSOCKETS FUNCTIONS
//
//
function open_websocket(hostname, hostport, hosturl) {

	dbg('Attempting to open web socket',true);
	function show_message(message) {
		show_server_msg(message);		
	}	
	var websocket_address = "ws://" + hostname + ":" + hostport + "/websocket/" + hosturl;
	ws = new WebSocket(websocket_address);
	
	ws.onopen = function() {		
		dbg('web socket open', debug_websocket);		
	};

	ws.onmessage = function(event) {		
		dbg('incomming message', debug_websocket);
		server_message_handler(event.data);
	};
	ws.onclose = function() {		
		dbg('closing websockets', debug_websocket);		
	};
}

function server_message_handler(data){
	var JsonData;
	dbg('server_message_handler(' + data +")", debug_websocket);
	try {
		JsonData = JSON.parse(data);
		dbg('JsonData = ' + JsonData);
	} catch(e) {
		dbg('JSON.parse error: "' + e + '". JsonData = ' + JsonData);
		return;
	}
}


function connect_to_websocket_host(){
	var hostname = "127.0.0.1";
	var hostport = "8888";
	var hosturl  = "ws";
	dbg('Pressed button: button_connect: [host, port] ' + hostname +':' + hostport + '/websocket/'+ hosturl, true);
	open_websocket(hostname, hostport, hosturl);
}

$(document).ready(function() {
	dbg('Document ready', true);
	connect_to_websocket_host();	
	// ws.onopen = function() {
 //   		ws.send("Hello, world");
	// };
	// ws.onmessage = function (evt) {
 //        alert(evt.data);
 //    };

///////////////////////////////////////////////////////////////////////
// MAIN GUI - jQUERY
//
//

});
