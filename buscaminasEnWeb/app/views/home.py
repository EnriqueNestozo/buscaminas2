#! /usr/bin/env python35
from flask import render_template,request, redirect, url_for, g, session
from flask_socketio import join_room, leave_room
from app import app, socketio
from app.static import *
import os
from app.static.models2 import *
from app.static.Usuario import Usuario
from collections import OrderedDict
import random

sesiones = []

listaConectados = OrderedDict()

@socketio.on('connect')
def connect():
	print("conectado: " + request.sid)

@socketio.on('ready')
def ready(usuario):
	if usuario['user']==None:
		print("usuario none")
		print("id usuario conectado: "+ request.sid + " es de: " + str(session['user']))
		listaConectados.update({str(session['user']) : request.sid})
		print(listaConectados)
		socketio.emit('connected',{'idSocket': request.sid})
		socketio.emit('usersConnected',listaConectados)
	else:
		print("usuario recuperado")
		print("id usuario conectado: "+ request.sid + " es de: " + usuario['user'])
		listaConectados.update({usuario['user'] : request.sid})
		print(listaConectados)
		socketio.emit('connected',{'idSocket': request.sid})
		socketio.emit('usersConnected',listaConectados)
    

@socketio.on('disconnect')
def disconnect():
	for name,socketid in listaConectados.items():
		if socketid == request.sid:
			print('usuario desconectado:' + name)
			listaConectados.pop(name)
			socketio.emit('usersConnected',listaConectados)
			break

@socketio.on('peticionDePartida')
def message(data):
	for name,socketid in listaConectados.items():
		print("buscando")
		if name == data['enviador']:
			print("emitiendo a socket")
			socketio.emit('solicitudDePartida',{'mensaje':'El jugador ' + data['enviador'] + ' desea comenzar una partida con usted', 'player1':data['enviador']}, room=data['receptor'])


@socketio.on('respuesta')
def respuesta(res):
	for name,socketid in listaConectados.items():
		if socketid == res['receptor']:
			socketio.emit('partidaNegada',{'mensaje':'El jugador rechazó la partida'}, room=socketid)


@socketio.on('redirectToGame')
def redirect_to_game(partida):
	print("redireccionando")
	socketio.emit('partidaAceptada',partida,room=partida['jugador1'])


jugador = True

@socketio.on('join')
def on_join(data):
	global jugador
	username = data['username']
	room = data['room']
	join_room(room)
	socketio.emit("mensaje", {'texto': username + ' has entered the room.', "miJugador":jugador, 'jugador': username}, room=room)
	jugador = not jugador

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    print(username + " leave the room " + room)
    send(username + ' has left the room.', room=room)

@socketio.on('ganador')
def ganador(data):
	if(buscarEnListaDePartidas(data['gana'])):
		print("usuario ganador esta: " + data['gana'])
		print(actualizar(data['gana'],True))
	else:
		print("usuario ganador no está")
		print(crearListaUsuario(data['gana']))
		print(actualizar(data['gana'],True))

	if(buscarEnListaDePartidas(data['pierde'])):
		print("usuario perdedor esta: " + data['pierde'])
		print(actualizar(data['pierde'],False))
	else:
		print("usuario perdedor no esta")
		print(crearListaUsuario(data['pierde']))
		print(actualizar(data['pierde'],False))

@socketio.on('mensajeDesdeRoom')
def mensaje_desde_room(data):
	socketio.emit("respuestaRoom",{'menssage':data['mensaje']}, room=data['room'])

@socketio.on('solicitarTablero')
def solicitar_tablero(data):
	socketio.emit("tableroGenerado",{'tablero': generar_tablero()},room=data['room'])


@socketio.on('tiro')
def tiro(data):
	socketio.emit("envioDeTiro",{'casilla':data['casilla'],'user':data['user']},broadcast=True,room=data['room'],include_self=False)


@socketio.on("cambiarTurno")
def cambiar_turno(data):
	turno = 0
	if data['turnoActual'] == "1":
		turno = 2
	else:
		turno = 1
	socketio.emit('respuestaTurno',{'turno':turno},room=data['room'])

@socketio.on('enviarMiUsuario')
def enviar_mi_usuario(data):
	socketio.emit('recibirUsuario',{'usuario':data['username']},broadcast=True,room=data['room'], include_self=False)

@socketio.on('solicitudRanking')
def solicitud_de_ranking():
	lista = []
	lista = obtenerMejoresJugadores()
	print (lista)

def generar_tablero():
	tablero = [[0] * 10 for i in range(10)]
	tablero = asignar_minas(tablero)
	tablero = asignar_numeros(tablero)
	return tablero


def asignar_minas(tablero):
	minas = 21
	for i in range(minas):
		is_bomb = False
		while not is_bomb:
			x = random.randint(0, len(tablero) -1)
			y = random.randint(0, len(tablero) - 1)
			if tablero[x][y] !=9:
				tablero[x][y] = 9
				is_bomb = True
	return tablero

def asignar_numeros(tablero):
	for x in range(len(tablero)):
		for y in range(len(tablero[x])):
			if tablero[x][y] == 9:
				tablero = verificar_abajo_izquierda(tablero, x, y)
				tablero = verificar_abajo(tablero,x,y)
				tablero = verificar_abajo_derecha(tablero,x,y)
				tablero = verificar_arriba_izquierda(tablero,x,y)
				tablero = verificar_arriba(tablero,x,y)
				tablero = verificar_arriba_derecha(tablero,x,y)
				tablero = verificar_izquierda(tablero,x,y)
				tablero = verificar_derecha(tablero,x,y)
	return tablero

def verificar_abajo_izquierda(tablero,x,y):
	if x + 1 < len(tablero[x]) and y - 1 >= 0 and tablero[x+1][y-1] != 9:
		tablero[x+1][y-1] +=1
	return tablero

def verificar_abajo(tablero,x,y):
	if x + 1 < len(tablero[0]) and tablero[x+1][y] !=9:
		tablero[x+1][y] +=1
	return tablero

def verificar_abajo_derecha(tablero,x,y):
	if x + 1 < len(tablero[0]) and y + 1 < len(tablero) and tablero[x+1][y+1] != 9:
		tablero[x+1][y+1] +=1
	return tablero

def verificar_arriba_izquierda(tablero,x,y):
	if x -1 >=0 and y - 1 >=0 and tablero[x-1][y-1] != 9:
		tablero[x-1][y-1] +=1
	return tablero

def verificar_arriba(tablero,x,y):
	if x - 1 >=0 and tablero[x-1][y] != 9:
		tablero[x-1][y] +=1
	return tablero

def verificar_arriba_derecha(tablero,x,y):
	if x - 1 >=0 and y + 1 < len(tablero) and tablero[x-1][y+1] != 9:
		tablero[x-1][y+1] +=1
	return tablero

def verificar_izquierda(tablero,x,y):
	if y - 1 >=0 and tablero[x][y-1] != 9:
		tablero[x][y-1] +=1
	return tablero

def verificar_derecha(tablero,x,y):
	if y + 1 < len(tablero) and tablero[x][y+1] != 9:
		tablero[x][y+1] +=1
	return tablero

@socketio.on('obtenerPerfil')
def obtener_perfil(data):
	user = (obtenerPerfilUsuario(data['user']))
	print(user)


app.secret_key = os.urandom(24)

@app.route('/game/<room>')
def game(room):
	if g.user:
		return render_template('game.html')
	return redirect(url_for('home'))

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'not logged in'

@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return 'Dropped'

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']


@app.route('/protected')
def protected():
	if g.user:
		return render_template('protected.html')
	return redirect(url_for('home'))


@app.route('/', methods=['GET', 'POST'])
def home():
	error = None
	if request.method == "GET":
		return render_template('home.html')
	elif request.method == 'POST':
		session.pop('user', None)
		nuevo_usuario = Usuario(request.form['usuario'], request.form['password'],"")
		if comprobarUsuario(nuevo_usuario):
			session['user'] = request.form['usuario']
			sesiones.append(request.form['usuario'])
			return redirect(url_for('protected'))
		else:
			error = 'Invalid username or password. Please try again!'
			return render_template('home.html', error=error)
        
@app.route('/signUp', methods=['GET', 'POST'])
def sign_up():
	error = None
	if request.method == "GET":
		return render_template('signUp.html')
	elif request.method == "POST":
		if(request.form['password'] == request.form['password2']):
			if(comprobarExistenciaUsuario(request.form['usuario'])):
				error="Ese usuario ya existe, porfavor elija otro nombre"
				return render_template('signUp.html', error=error)
			else:
				nuevo_usuario = Usuario(request.form['usuario'],request.form['password'],request.form['email'])
				crearUsuario(nuevo_usuario)
				error = "usuario creado exitosamente"
				return render_template('signUp.html', error=error)
		else:
			error="Las contraseñas no coinciden"
			return render_template("signUp.html", error=error)
