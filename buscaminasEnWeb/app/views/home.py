#! /usr/bin/env python35
from flask import render_template,request, redirect, url_for, g, session
from app import app, socketio
from app.static import *
import os
from app.static.models2 import *
from app.static.Usuario import Usuario


sesiones = []
"""
@app.route('/')
def home():
	return render_template('home.html')



app.secret_key = os.urandom(24)
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
			return redirect(url_for('protected'))
		else:
			error = 'Invalid username or password. Please try again!'
			return render_template('home.html', error=error)
	        #if 'user already exist in database':
	        #    return "user authenticated"
	        #else:
	        #	return "user invalid"
        
"""

@app.route('/protected/<myId>')
def protected(myId):
	print('en protected')
	if myId in sesiones:
		print("usuario paso")
		return render_template('protected.html')
	else:
		print("usuario no permitido")

"""
@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.route('/getsession')
def getsession():
	if 'user' in session:
		return session['user']
	return 'not logged in'

@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return 'Dropped'
"""
@socketio.on('requestPage')
def requestPage(myId):
	if myId in sesiones:
		print ('requestPage ' + myId)
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
		socketio.emit('respuestaVerificacion', { 're':'True', 'id':usuario['nombre']})
	else:
		socketio.emit('respuestaVerificacion', {'re':'Nombre de usuario y/o contraseña inválido'})




