const remote = require('electron').remote
const main = remote.require('./main.js')

document.getElementById('regresarBtn').onclick = function(){
	main.openWindow('index')
}

document.getElementById('signInBtn').onclick = function(){
	main.openWindow('menu')
}

/*
document.getElementById('signInBtn').onclick = function(){
	var username = document.getElementById('nombreUsuario').value;
	var password1 = document.getElementById('Password1').value;
}
*/