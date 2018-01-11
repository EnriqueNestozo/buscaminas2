#! /usr/bin/env python35
from flask import render_template,request, redirect, url_for, g, session
from app import app, socketio
from app.static import *
import os
from app.static.models2 import *
from app.static.Usuario import Usuario
from collections import OrderedDict


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
    print("usuario conectado"+ request.sid)
    listaConectados.update({str(session['user']) : request.sid})
    print(listaConectados)
    socketio.emit('connected',{'idSocket': request.sid})
    socketio.emit('usersConnected',listaConectados)

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


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

@socketio.on('sesion')
def sesion():
	listaDeSesiones = ' '.join(map(str, sesiones))
	print(listaDeSesiones)
	socketio.emit('respuestaSesion', {'re': listaDeSesiones})

app.secret_key = os.urandom(24)

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
