var myUser="";
var users="";
var mySocket=null;
var arrayDeSockets = []

var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connected',function(info){
	if(mySocket==null){
		mySocket = info.idSocket;
		console.log('mi socket es: ' + mySocket)
	}
});

socket.on('usersConnected', function(sockets){
	for (var key in sockets) {
		if(myUser==""){
			if(sockets[key] == mySocket){
				myUser = key
				console.log("mi usuario es: " + myUser)
			}
		}	
	}
	for(var key in sockets){
		if(key != myUser){
			console.log("Key: " + key);
    		console.log("Value: " + sockets[key]);
		}
	}
});

/*for(var i=0; i<Object.keys.length;i++){
			if(key != myUser){
				console.log("Key: " + key);
	    		console.log("Value: " + sockets[key]);
			}
			
		}
*/