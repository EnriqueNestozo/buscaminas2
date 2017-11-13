const remote = require('electron').remote
const main = remote.require('./main.js')

document.getElementById('Registro').onclick = function(){
	main.openWindow('registro')
}

document.getElementById('Sesion').onclick = function(){
	main.openWindow('sesion')
}
