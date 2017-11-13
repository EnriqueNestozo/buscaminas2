#! /usr/bin/env python35
import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from businesslogic.models import *
from businesslogic.Usuario import Usuario
from flask_socketio import join_room, leave_room


sio = socketio.Server()
app = Flask(__name__)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)

@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('comprobar-usuario')
def comprobacion_de_usuario(sid,usuario):
    nuevoUsuario = Usuario(usuario['nombre'],usuario['contrasena'])
    respuesta = comprobarUsuario(nuevoUsuario.getName())
    if(respuesta == False):
        usuarioCreado = crearUsuario(nuevoUsuario)
        if(usuarioCreado == True):
            sio.emit('respuesta-registro',{
                'mensaje': 'Usuario creado existosamente'
            })
        else:
            sio.emit('respuesta-registro',{'mensaje': 'No se pudo crear el usuario correctamente'}) 
    else:
        sio.emit('respuesta-registro',{
            'mensaje': 'usuario ya registrado, porfavor introduzca otro nombre'
        })
    

'''
@sio.on('registrar-usuario')
def registrar(sid,usuarioNuevo):
    user = Usuario(usuarioNuevo['nombre'],usuarioNuevo['contrasena'])
    respuesta = crearUsuario(user)
'''

@sio.on('new-message')
def handle_my_custom_event(sid, mensaje):
    print('received json: ' + str(mensaje['author']))
    print('received json: ' + str(mensaje['text']))
    sio.emit('respuesta', str(mensaje['author']),str(mensaje['text']))

if __name__ == '__main__':
    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

@sio.on('solicitar-nuevo-tablero')
def nuevo_tablero(sid,mensaje)