const remote = require('electron').remote
const main = remote.require('./main.js')

document.getElementById('Jugar').onclick = function(){
	main.open('menuJugar')
}