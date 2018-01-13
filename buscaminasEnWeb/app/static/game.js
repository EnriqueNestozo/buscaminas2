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
            //mandar nuevo array al otro usuario y el turno
        }
    }		    
    
}

function mostrarNumero(e){
	var auxstr = this.id.split("");				
	var myid = auxstr[0] + auxstr[1];			
	divObj = document.getElementById(myid);
	var fila = tableroEnArray[auxstr[0]];
	if(fila[auxstr[1]] == 0){
		divObj.style.backgroundColor = "#818181";
		//Aqui sustituyo el valor por un - para saber que ya se tiro ahi (debo hacer lo mismo para las casillas que se abrieron)
		tableroEnArray[auxstr[0]][auxstr[1]] = "-"
		abrirAlrededor(auxstr[0],auxstr[1])
	}else{
		if(fila[auxstr[1]] != 9 && !isNaN(fila[auxstr[1]])){
			document.getElementById(myid).innerHTML = "<p style='margin-top:15px;'>" + fila[auxstr[1]] + "</p>";
			divObj.style.backgroundColor = "#818181";
			//Aqui sustituyo el valor por un - para saber que ya se tiro ahi 
			tableroEnArray[auxstr[0]][auxstr[1]] = "-"
		}else{
			if(fila[auxstr[1]] == 9){
				tableroEnArray[auxstr[0]][auxstr[1]] = "x"
				divObj.style.backgroundColor = "#818181";
				divObj.style.backgroundImage = "url(/static/mina.png)";
			}else{
				alert("Por favor tira en una casilla que no haya sido abierta")
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