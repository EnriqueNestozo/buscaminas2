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
"""
@app.route('/protected')
@login_required
def protected():
	print('en protected')
	if myId in sesiones:
		print("usuario paso")
		return render_template('protected.html')
	else:
		print("usuario no permitido")


@app.before_request
def before_request():
	g.user = None
	if 'user' in sesiones:
		g.user = sesiones['user']


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@socketio.on('requestPage')
def requestPage():
		destination = '/protected.html'
		socketio.emit('redirectToPrincipal',{'url':'/protected'})

@app.route('/')
def home():
	return render_template('home.html')

@socketio.on('connect')
def connect():
    print("usuario conectado"+ request.sid)

@socketio.on('disconnect')
def disconnect():
	print('usuario desconectado')

@socketio.on('verificacionUsuario')
def verificacion(usuario):
	nuevoUsuario = Usuario(usuario['nombre'], usuario['contrasena'],"")
	if comprobarUsuario(nuevoUsuario):
		print("usuario verificado " + usuario['nombre'])
		sesiones.append(usuario['nombre'])
		g.user = usuario['nombre']
		socketio.emit('respuestaVerificacion', { 're':'True', 'id':usuario['nombre']})
	else:
		socketio.emit('respuestaVerificacion', {'re':'Nombre de usuario y/o contraseña inválido'})

"""
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
	
    
##creo que no se usa
@socketio.on('requestUsersConnected')
def usersConnected():
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


"""
@socketio.on('sesion')
def sesion():
	listaDeSesiones = ' '.join(map(str, sesiones))
	print(listaDeSesiones)
	socketio.emit('respuestaSesion', {'re': listaDeSesiones})




"""

@socketio.on('respuesta')
def respuesta(res):
	for name,socketid in listaConectados.items():
		if socketid == res['receptor']:
			socketio.emit('partidaNegada',{'mensaje':'El jugador rechazó la partida'}, room=socketid)


@socketio.on('redirectToGame')
def redirectToGame(partida):
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
    send(username + ' has left the room.', room=room)

@socketio.on('mensajeDesdeRoom')
def mensajeDesdeRoom(data):
	socketio.emit("respuestaRoom",{'menssage':data['mensaje']}, room=data['room'])

@socketio.on('solicitarTablero')
def solicitarTablero(data):
	socketio.emit("tableroGenerado",{'tablero': generarTablero()},room=data['room'])


@socketio.on('tiro')
def tiro(data):
	socketio.emit("envioDeTiro",{'casilla':data['casilla'],'user':data['user']},broadcast=True,room=data['room'],include_self=False)

"""
turno = False
@socketio.on('preguntarTurno')
def turno(data):
	global turno
	print("turno: "+turno)
	if turno:
		turnoDe = 1
	else:
		turnoDe = 2
	emit('respuestaTurno',{'turno': turnoDe},room=data['room'], callback=)
	turno = not turno
"""
@socketio.on("cambiarTurno")
def cambiarTurno(data):
	turno = 0
	if data['turnoActual'] == "1":
		turno = 2
	else:
		turno = 1
	socketio.emit('respuestaTurno',{'turno':turno},room=data['room'])

@socketio.on('enviarMiUsuario')
def enviarMiUsuario(data):
	socketio.emit('recibirUsuario',{'usuario':data['username']},broadcast=True,room=data['room'], include_self=False)

def generarTablero():
	tablero = [[0] * 10 for i in range(10)]
	tablero = asignarMinas(tablero)
	tablero = asignarNumeros(tablero)
	return tablero


def asignarMinas(tablero):
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

def asignarNumeros(tablero):
	for x in range(len(tablero)):
		for y in range(len(tablero[x])):
			if tablero[x][y] == 9:
				tablero = verificarAbajoIzquierda(tablero, x, y)
				tablero = verificarAbajo(tablero,x,y)
				tablero = verificarAbajoDerecha(tablero,x,y)
				tablero = verificarArribaIzquierda(tablero,x,y)
				tablero = verificarArriba(tablero,x,y)
				tablero = verificarArribaDerecha(tablero,x,y)
				tablero = verificarIzquierda(tablero,x,y)
				tablero = verificarDerecha(tablero,x,y)
	return tablero

def verificarAbajoIzquierda(tablero,x,y):
	if x + 1 < len(tablero[x]) and y - 1 >= 0:
		if tablero[x+1][y-1] != 9:
			tablero[x+1][y-1] +=1
	return tablero

def verificarAbajo(tablero,x,y):
	if x + 1 < len(tablero[0]):
		if tablero[x+1][y] != 9:
			tablero[x+1][y] +=1
	return tablero

def verificarAbajoDerecha(tablero,x,y):
	if x + 1 < len(tablero[0]) and y + 1 < len(tablero):
		if tablero[x+1][y+1] != 9:
			tablero[x+1][y+1] +=1
	return tablero

def verificarArribaIzquierda(tablero,x,y):
	if x -1 >=0 and y - 1 >=0:
		if tablero[x-1][y-1] != 9:
			tablero[x-1][y-1] +=1
	return tablero

def verificarArriba(tablero,x,y):
	if x - 1 >=0:
		if tablero[x-1][y] != 9:
			tablero[x-1][y] +=1
	return tablero

def verificarArribaDerecha(tablero,x,y):
	if x - 1 >=0 and y + 1 < len(tablero):
		if tablero[x-1][y+1] != 9:
			tablero[x-1][y+1] +=1
	return tablero

def verificarIzquierda(tablero,x,y):
	if y - 1 >=0:
		if tablero[x][y-1] != 9:
			tablero[x][y-1] +=1
	return tablero

def verificarDerecha(tablero,x,y):
	if y + 1 < len(tablero):
		if tablero[x][y+1] != 9:
			tablero[x][y+1] +=1
	return tablero



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
		nuevoUsuario = Usuario(request.form['usuario'], request.form['password'],"")
		if comprobarUsuario(nuevoUsuario):
			session['user'] = request.form['usuario']
			sesiones.append(request.form['usuario'])
			return redirect(url_for('protected'))
		else:
			error = 'Invalid username or password. Please try again!'
			return render_template('home.html', error=error)
	        #if 'user already exist in database':
	        #    return "user authenticated"
	        #else:
	        #	return "user invalid"
        
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
	error = None
	if request.method == "GET":
		return render_template('signUp.html')
	elif request.method == "POST":
		if(request.form['password'] == request.form['password2']):
			if(comprobarExistenciaUsuario(request.form['usuario'])):
				error="Ese usuario ya existe, porfavor elija otro nombre"
				return render_template('signUp.html', error=error)
			else:
				nuevoUsuario = Usuario(request.form['usuario'],request.form['password'],request.form['email'])
				crearUsuario(nuevoUsuario)
				error = "usuario creado exitosamente"
				return render_template('signUp.html', error=error)
		else:
			error="Las contraseñas no coinciden"
			return render_template("signUp.html", error=error)
