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
	//quitar
	console.log(data.texto)
	console.log(data.miJugador)
	if(myUser == ""){
		if(data.miJugador){
			myUser = 1;
			document.getElementById("nombre1").innerHTML = "<p style='margin-top:15px;font-size:30px;text-align:center;'>" + usuario.user + "</p>";
		}else{
			myUser = 2;
			document.getElementById("nombre2").innerHTML = "<p style='margin-top:15px;font-size:30px;text-align:center;'>" + usuario.user + "</p>";
		}
		//quitar
		console.log(myUser)
	}else{
		//quitar
		console.log("aqui")
		document.getElementById("nombre2").innerHTML = "<p style='margin-top:15px;font-size:30px;text-align:center;'>" + data.jugador + "</p>";
		socket.emit('enviarMiUsuario',partida);
	}
	numOfUsers+=1;
	if(numOfUsers>1){
		socket.emit('solicitarTablero',partida)	
	}
	socket.on('recibirUsuario',function(data){
		//quitar
		console.log("recibi usuario")
		document.getElementById("nombre1").innerHTML = "<p style='margin-top:15px;font-size:30px;text-align:center;'>" + data.usuario + "</p>";
	});
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

function crearTablero(tablero){
	crearCasillas()
}


function crearCasillas(){
	for(var i = 0; i < 10; i++){
        for(var j = 0; j < 10; j++){			           
           var div = document.createElement("div");
            div.id = i + "" + j;			            
            div.addEventListener("click",function(){
            	verificarTurno(this.id,myUser)},true);
            var tablerominas = document.getElementById("tablerominas");      
            tablerominas.appendChild(div);
        }
    }		    
    
}

function deshabilitarCasillas(){
	document.getElementById("turno").innerHTML = 0
}


socket.on("respuestaTurno",function(data){
	console.log(data)
	document.getElementById("turno").innerHTML = data.turno
});

function verificarTurno(id,myUser){
	var turno = document.getElementById("turno").innerHTML
	var dato = {
		room:roomKey,
		turnoActual: turno
	}
	if(myUser == turno){
		if(document.getElementById(id).textContent == "" || document.getElementById(id).style.backgroundImage == ""){
			if(mostrarNumero(id,myUser) == false){
				socket.emit("cambiarTurno",dato)
			}
		}
		
	}else if(turno==0){
		alert("partida terminada")
	}else{
		alert("No te toca")
	}
	/*
	socket.emit('preguntarTurno',{'room':roomKey},function(data){
		if(data.turno == myUser){
			mostrarNumero(id,myUser);
		}else{
			alert("No te toca");
		}
	});
	*/
};

socket.on("envioDeTiro",function(data){
	mostrarNumero(data.casilla,data.user)
});

function mostrarNumero(id,user){
	var auxstr = id.split("");			
	var myid = auxstr[0] + auxstr[1];

	var envio ={
		casilla:myid,
		room : roomKey,
		user : myUser
	}

	divObj = document.getElementById(myid);
	var fila = tableroEnArray[auxstr[0]];
	if(fila[auxstr[1]] == 0){
		divObj.style.backgroundColor = "#818181";
		//Aqui sustituyo el valor por un - para saber que ya se tiro ahi (debo hacer lo mismo para las casillas que se abrieron)
		tableroEnArray[auxstr[0]][auxstr[1]] = "-"
		socket.emit("tiro",envio)
		abrirAlrededor(parseInt(auxstr[0]),parseInt(auxstr[1]))
		return false
	}else{
		if(fila[auxstr[1]] != 9 && !isNaN(fila[auxstr[1]])){
			document.getElementById(myid).innerHTML = "<p style='margin-top:15px;'>" + fila[auxstr[1]] + "</p>";
			divObj.style.backgroundColor = "#818181";
			//Aqui sustituyo el valor por un - para saber que ya se tiro ahi 
			tableroEnArray[auxstr[0]][auxstr[1]] = "-"
			socket.emit("tiro",envio)
			return false
		}else{
			if(fila[auxstr[1]] == 9){
				if(user == 1){
					tableroEnArray[auxstr[0]][auxstr[1]] = "x"
					divObj.style.backgroundColor = "#818181";
					divObj.style.backgroundImage = "url(/static/mina.png)";
					socket.emit("tiro",envio)
					comprobarMinas();
					return true
					
				}else{
					tableroEnArray[auxstr[0]][auxstr[1]] = "Y"
					divObj.style.backgroundColor = "#818181";
					divObj.style.backgroundImage = "url(/static/minared.png)";
					socket.emit("tiro",envio)
					comprobarMinas();
					return true

				}
				
			}
		}
	}
	console.log(tableroEnArray)						
};

function abrirAlrededor(fila,pos){
	if(fila==0 && pos==0){
		abrirCeros(fila,pos,fila+1,pos+1,fila,pos);
	}else if(fila==0 && (pos>0 && pos <9)){
		abrirCeros(fila,pos-1,fila+1,pos+1,fila,pos);
	}else if(fila==0 && pos==9){
		abrirCeros(fila,pos-1,fila+1,pos,fila,pos);
	}else if(pos==9 && (fila>0 && fila<9)){
		abrirCeros(fila-1,pos-1,fila+1,pos,fila,pos);
	}else if(fila==9 && pos ==9){
		abrirCeros(fila-1,pos-1,fila,pos,fila,pos);
	}else if(fila==9 && (pos>0 && pos<9)){
		abrirCeros(fila-1,pos-1,fila,pos+1,fila,pos);
	}else if(fila==9 && pos==0){
		abrirCeros(fila-1,pos,fila,pos+1,fila,pos);
	}else if(pos==0 && (fila>0 && fila<9)){
		abrirCeros(fila-1,pos,fila+1,pos+1,fila,pos);
	}else{
		abrirCeros(fila-1,pos-1,fila+1,pos+1,fila,pos);
	}
};

function abrirCeros(var1,var2,var3,var4,var5,var6){
	console.log(var1)
	console.log(var2)
	console.log(var3)
	console.log(var4)
	console.log(var5)
	console.log(var6)
	for(var i = var1; i<=var3;i++){
		for(var j = var2; j<=var4;j++){
			var myid = i + "" + j;
			var objDiv = document.getElementById(myid);
			if(objDiv.textContent == ""){
				if(tableroEnArray[i][j] == 0){
					if(i == var5 && j == var6){
						objDiv.textContent = ""	;
						objDiv.style.backgroundColor = "#818181";
						tableroEnArray[i][j] = "-"
					}else{
						if(objDiv.style.backgroundColor != "#818181"){
							abrirAlrededor(i, j);
						}
					}
				}else{
					if(tableroEnArray[i][j] !=9){
						document.getElementById(myid).innerHTML = "<p style='margin-top:15px;'>" + tableroEnArray[i][j] + "</p>";
						objDiv.style.backgroundColor = "#818181";
						tableroEnArray[i][j] = "-"
					}
				}
			}
		}
	}

};	

function comprobarMinas(){
	var misMinas=0;
	var minasContrario=0;
	for(var i=0;i<10;i++){
		for(var j=0;j<10;j++){
			if(tableroEnArray[i][j] == "x"){

				if(myUser==1){
					misMinas+=1;
					console.log("mis minas como jugador1-azul" +misMinas)
					document.getElementById("mina1").innerHTML = "<p style='margin-top:15px;font-size:20px;text-align:center;'>" + misMinas + "</p>";
				}else{
					minasContrario+=1;
					console.log("minas contrario como jugador2-rojo" +minasContrario)
					document.getElementById("mina1").innerHTML = "<p style='margin-top:15px;font-size:20px;text-align:center;'>" + minasContrario + "</p>";
				}
			}
			if(tableroEnArray[i][j]== "Y"){
				if(myUser==2){
					misMinas+=1;
					console.log("mis minas como jugador2-rojo"+misMinas)
					document.getElementById("mina2").innerHTML = "<p style='margin-top:15px;font-size:20px;text-align:center;'>" + misMinas + "</p>";
				}else{
					minasContrario+=1;
					console.log("minas contrario como jugador1-azul" +minasContrario)
					document.getElementById("mina2").innerHTML = "<p style='margin-top:15px;font-size:20px;text-align:center;'>" + minasContrario + "</p>";
				}
			}
		}
	}
	verificarGanador(misMinas,minasContrario)
};

function verificarGanador(misMinas,minasContrario){
	if(misMinas > 3){
		if(myUser==1){
			var ganador = document.getElementById("nombre1").textContent
			var perdedor = document.getElementById("nombre2").textContent
			var jugadorGanador ={
				gana:ganador,
				pierde:perdedor 
			}
			socket.emit("ganador",jugadorGanador);
			alert("El jugador " + ganador + " ha ganado")
			deshabilitarCasillas()			
		}else{
			var ganador = document.getElementById("nombre2").textContent
			alert("El jugador " + ganador + " ha ganado")
			deshabilitarCasillas()
		}
	}
	if(minasContrario > 3){
		if(myUser==2){
			var ganador = document.getElementById("nombre1").textContent
			alert("El jugador " + ganador + " ha ganado")
			deshabilitarCasillas()
		}else{
			var ganador = document.getElementById("nombre2").textContent
			var perdedor = document.getElementById("nombre1").textContent
			var jugadorGanador ={
				gana:ganador,
				pierde:perdedor
			}
			socket.emit("ganador",jugadorGanador);
			alert("El jugador " + ganador + " ha ganado")
			deshabilitarCasillas()
		}	
	}
	
};


document.getElementById("salir").onclick = function(){
	window.location = "/protected"
}