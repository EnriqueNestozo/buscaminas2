var myUser="";
var users="";
var mySocket=null;
var arrayDeIds = [];
var socket;
var usuario = {
	user : sessionStorage.getItem('user')
};

socket = io.connect('http://' + document.domain + ':' + location.port,usuario);

socket.emit('ready',usuario)

socket.on('connected',function(info){
	if(mySocket==null){
		mySocket = info.idSocket;
		console.log('mi socket es: ' + mySocket)
	}
});

socket.on('usersConnected', function(sockets){
	users = sockets;
	for (var key in sockets) {
		if(myUser==""){
			if(sockets[key] == mySocket){
				myUser = key
				console.log("mi usuario es: " + myUser)
				var usuario = {
					user : sessionStorage.setItem('user',myUser)
				}
			}
		}	
	}
	for(var key in sockets){
		if(key != myUser){
			if(arrayDeIds.includes(key)){

			}else{
				document.getElementById("conectados").innerHTML += "<div class='card' onClick='preguntar(this.id)' id='"+ key + "'><div class='card-block'><h4 class='card-title'>" + key + "</h4></div></div>"
				console.log("Key: " + key);
	    		console.log("Value: " + sockets[key]);
	    		arrayDeIds.push(key);
			}
		}
	}
	quitarDesconectados(sockets);
});

socket.on('solicitudDePartida',function(solicitud){
	if(confirm(solicitud.mensaje)){
		for(var key in users){
			if(key == solicitud.player1){
				var partida ={
					idRoom: mySocket+users[key],
					jugador1:users[key],
					jugador2:myUser
				};
				socket.emit('redirectToGame',partida)
				window.location.href = 'http://' + document.domain + ':' + location.port + '/game/' + partida.idRoom
			}
		}
		
	}else{
		for(var key in users){
			if(key == solicitud.player1){
				var mensaje = {
					enviador: myUser,
					receptor: users[key]
				};
			}
		}
		
		socket.emit('respuesta',mensaje)
	}
});

socket.on('partidaNegada',function(respuesta){
	console.log(respuesta)
	alert(respuesta.mensaje)
});

socket.on('partidaAceptada',function(respuesta){
	window.location.href = 'http://' + document.domain + ':' + location.port + '/game/' + respuesta.idRoom
})


function quitarDesconectados(sockets){
	for(i=0;i<arrayDeIds.length;i++){
		if(arrayDeIds[i] in sockets){

		}else{
			var elemento = document.getElementById(arrayDeIds[i]);
			if(elemento !=null){
				elemento.parentNode.removeChild(elemento);
				arrayDeIds.splice(i, 1)
			}
		}
	}
};

function preguntar(idDiv){
	for(var key in users){
		if(idDiv == key){
			var mensaje = {
				enviador: myUser,
				receptor: users[key]
			};
			socket.emit('peticionDePartida',mensaje);
			console.log("Preguntar a: " + users[key])
		}
	}
	
}


/*for(var i=0; i<Object.keys.length;i++){
			if(key != myUser){
				console.log("Key: " + key);
	    		console.log("Value: " + sockets[key]);
			}
			
		}
*/