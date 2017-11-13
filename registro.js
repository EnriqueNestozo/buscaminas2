const remote = require('electron').remote
const main = remote.require('./main.js')

/*
const zerorpc = require("zerorpc")
let client = new zerorpc.Client()
client.invoke("echo", "server ready", (error, res) => {
  if(error || res !== 'server ready') {
    console.error(error)
  } else {
    console.log("server is ready")
  }
})
*/

document.getElementById('signUpBtn').onclick = function(){
	var username = document.getElementById('nombreUsuario').value;	
	var password1 = document.getElementById('Password1').value;
	var password2 = document.getElementById('Password2').value;
	if(password1 == "" || password2 =="" || username ==""){
		window.alert("Debes llenar todos los campos")
	}else if( password1 == password2){
		respuesta = registrarUsuario(username,password1);	
	}else{
		window.alert('Las contrasenas no coinciden, porfavor ingresalas correctamente')
	}

	//addMessage()
};

function addMessage() {
	var mensaje = {
    author: document.getElementById('nombreUsuario').value,
    text: document.getElementById('Password1').value
  };

  socket.emit('new-message', mensaje);
  return false;
};

document.getElementById('regresarBtn').onclick = function(){
	socket.on('disconnect'), function(){}
	main.openWindow('index')
};

var registrarUsuario = function(username,password){
	var socket = io.connect('http://localhost:8000');
	var nuevoUsuario = {
		nombre: username,
		contrasena: password		
	};
	socket.emit('comprobar-usuario',nuevoUsuario);
	socket.on('respuesta-registro', function(estado){
		var respuesta = estado.mensaje;
	    window.alert(respuesta)
	});

};

/*
function registrar(username,password1){
	var nuevoUsuario = {
		nombre: username,
		contrasena: password1		
	};
	var socket = io.connect('http://localhost:8000');
	socket.emit('registrar-usuario',nuevoUsuario);
	respuesta = socket.on('respuesta')
	
	var usernameDot = username + "."
	console.log(usernameDot);/////////////
	var usuario = usernameDot.concat(password1)
	console.log(usuario);//////////
  	client.invoke("create_user", usuario, (error, res) => {
    if(error) {
      console.error(error)
    } else {
      window.alert('Usuario registrado exitosamente')
    }
  })
}
*/