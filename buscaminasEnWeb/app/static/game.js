var mySocket=null;
var myUser="";
var roomKey="";
var tableroEnArray=null
var numOfUsers = 0
var usuario = {
	user : sessionStorage.getItem('user')
};


var socket = io.connect('http://' + document.domain + ':' + location.port);

var patharray = window.location.pathname.split('/')
console.log(patharray[2])
roomKey = patharray[2]

var partida = {
	room : roomKey,
	username : usuario.user
}

socket.emit('join',partida)

socket.on("mensaje",function(data){
	console.log(data.texto)
	numOfUsers+=1;
	if(numOfUsers>1){
		socket.emit('solicitarTablero',partida)	
	}
});


socket.on('tableroGenerado',function(data){
	tableroEnArray = data.tablero
	console.log(tableroEnArray)
	crearTablero(tableroEnArray);
	for(var x=0; x<10; x++){
		for(var y=0; y<10;y++){
			var fila = data.tablero[x]
		}
	}
	
});

//Quitar
document.getElementById("mandar").onclick = function(){
	console.log(tableroEnArray[0])
	var mensaje={
		room:roomKey,
		mensaje: "hola"
	}
	socket.emit("mensajeDesdeRoom",mensaje)
};
///quitar
socket.on("respuestaRoom", function(data){
	console.log(data.menssage)
});

function crearTablero(tablero){
	crearCasillas()
}


function crearCasillas(){
	for(var i = 0; i < 10; i++){
        for(var j = 0; j < 10; j++){			           
           var div = document.createElement("div");
            div.id = i + "" + j;			            
            div.addEventListener("click",mostrarNumero, true);
            var tablerominas = document.getElementById("tablerominas");      
            tablerominas.appendChild(div);
        }
    }		    
    
}

function mostrarNumero(e){
	var auxstr = this.id.split("");				
	var myid = auxstr[0] + auxstr[1];			
	divObj = document.getElementById(myid);
	var fila = tableroEnArray[auxstr[0]];
	if(fila[auxstr[1]] == 0){
		divObj.style.backgroundColor = "white";
		tableroEnArray[auxstr[0]][auxstr[1]] = "x"
		console.log(tableroEnArray)
		//abrirAlrededor()
	}



	if(minas[parseInt(auxstr[0],10)][parseInt(auxstr[1],10)] == 0){
		divObj.style.backgroundColor = "white";					
		abrirAlrededor(parseInt(auxstr[0],10),parseInt(auxstr[1],10),minas);
	}else{
		if(minas[parseInt(auxstr[0],10)][parseInt(auxstr[1],10)] != "*"){
			document.getElementById(myid).innerHTML = "<p style='margin-top:15px;'>" + minas[parseInt(auxstr[0],10)][parseInt(auxstr[1],10)] + "</p>";
			divObj.style.backgroundColor = "white";
		}else{
			divObj.style.backgroundImage = "url(img/bomba.jpg)";						
			abrirTablero(minas);
			alert("Perdiste =(");
		}
	}						
}	