var mplayerSock;
function updateStatus(data){
	$("#status").html(data.status);
}
function showInfo(info){
	$("#status").html(info);
}
$(function() {
// setup master volume
	
// setup graphic EQ
$( "#eq > span" ).each(function() {
	// read initial values from markup and replace them with equalizer 
	var value = parseInt( $( this ).text(), 10 );
	$( this ).empty().slider({
		min : -12,
		max : 12,
		value: value,
		range: "min",
		animate: true,
		orientation: "vertical",
		stop: function(event, ui) {
			window.eqvals=[];
			$( "#eq > span" ).each(function(index,element) {
				window.eqvals.push($(element).slider("value"));
			} );
			$.post( "mplayer_api.py", JSON.stringify({ eq: window.eqvals, volumehelper: $("#master").slider("value")  }))
			.done(function( data ) {
				updateStatus(data)
			});
		}
	});
});
/*$( "#master" ).slider({
		value: window.volume,
		orientation: "horizontal",
		range: "min",
		animate: true,
		stop: function(event, ui) {
			$.post( "mplayer_api.py", JSON.stringify({ volume: ui.value, eqhelper: window.eqvals}))
			.done(function( data ) {
				updateStatus(data)
			});
	}
});*/

$("#startStreamBtn").click(function(event){
    //alert(JSON.stringify(constructInitObject($('#launcherForm').serializeArray())))
$.post( "mplayer_api.py", JSON.stringify(constructInitObject($('#launcherForm').serializeArray())))
			.done(function( data ) {
                                if (data.status=="starting"){
                                    
                                    mplayerSock=mplayerWebSocket();
                                }
                                    updateStatus(data)
                                
                                
			});
                    });
});
function mplayerWebSocket(){
	try{
		var ws = new WebSocket('wss://'+window.location.hostname+':7777');
	}catch(e){
		window.open('https://'+window.location.hostname+':7777', '_blank');
		updateStatus({status:'please add exception and refresh'});
	}
    ws.onopen = function() {
            $(".mplayerView").hide();
                                    $("#mplayerPlayView").show();
    updateStatus({status:'CONNECTED'});

  };
   ws.onclose = function() {
    updateStatus({status:'DISCONNECTED'});
  };
   ws.onmessage = function(event) {
    showInfo(event.data);
  };
  return ws
  

}