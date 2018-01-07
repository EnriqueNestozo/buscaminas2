var usuarios = [];
var points = [];
var myUser;

document.getElementById('btnIngresar').onclick = function(){
	var usuario = document.getElementById('usuario').value;
	var password = document.getElementById('password').value;
	if(usuario =='' || password == ''){
		alert("Debe llenar todos los campos");
	}else{
		iniciarSesion(usuario,password);
	}
};

document.getElementById('inicioSesion').onclick = function(){
	var formToHide = document.getElementById('formRegistro')
	var formToShow = document.getElementById('formInicioDeSesion')
	formToHide.style.display="none"
	formToShow.style.display="block"
	document.getElementById("inicioSesion").classList.add('active');
	document.getElementById("registro").classList.remove('active');
};

document.getElementById('registro').onclick = function(){
	var formToHide = document.getElementById('formInicioDeSesion')
	var formToShow = document.getElementById('formRegistro')
	formToHide.style.display="none"
	formToShow.style.display="block"
	document.getElementById("inicioSesion").classList.remove('active');
	document.getElementById("registro").classList.add('active');
};




var iniciarSesion = function(username,password){
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	var usuario = {
		nombre: username,
		contrasena: password
	};
	socket.emit('verificacionUsuario',usuario);
	socket.on('respuestaVerificacion',function(data){
		if(data.re == "True"){
			console.log("true");
			myUser = data.id;
			socket.emit('requestPage',myUser)
		}else{
			alert(data.re)
		};
	});
	socket.on('redirectToPrincipal', function(destination){
		console.log("redirectToPrincipal")
		window.location.href = destination.url;
	});
	
}