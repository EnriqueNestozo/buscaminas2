import socketio
import eventlet
import eventlet.wsgi
from flask import Flask, render_template
from models import *

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
    respuesta = comprobarUsuario(usuario['nombre'])
    sio.emit('respuesta-comprobacion-usuario',respuesta)

@sio.on('registrar-usuario')
def registrar(sid,user,password):
    

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