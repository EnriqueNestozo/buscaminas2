var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);
var zerorpc = require('zerorpc');

app.use(express.static('public'));

/*app.get('/', function(peticion, respuesta){
	respuesta.sendFile(__dirname + '/src/buscaminas_online-app/buscaminas_online-app.html');
})

app.use("/bower_components", express.static(__dirname + "/bower_components"));
*/
io.on('connection', function(socket){
	console.log("alguien se ha conectado")
})

server.listen(8090, function(){
	console.log('Servidor corriendo en http://localhost:8090');
});