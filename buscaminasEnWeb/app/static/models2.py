#! /usr/bin/env python35
from peewee import *
import hashlib

database = MySQLDatabase('buscaminas', **{'user': 'admin', 'password': 'qwertyasd'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    email = CharField(null=True)
    password = CharField()
    username = CharField(primary_key=True)

    class Meta:
        db_table = 'users'

class Listapartida(BaseModel):
    idpartida = PrimaryKeyField(db_column='idPartida')
    partidasganadas = IntegerField(db_column='partidasGanadas', null=True)
    partidastotales = IntegerField(db_column='partidasTotales', null=True)
    username = ForeignKeyField(db_column='username', null=True, rel_model=Users, to_field='username')

    class Meta:
        db_table = 'listapartida'

def crearUsuario(Usuario):
        try:
            with database.atomic():
                md5 = hashlib.md5()
                md5.update(Usuario.getPassword().encode('utf-8'))
                newPassword = md5.hexdigest()
                user = Users.create(username = Usuario.getName(), password = newPassword, email = Usuario.getEmail())
                user.save()
            return True
        except peewee.IntegrityError:
            return 'Error: %s No se pudo crear el usuario ' % Usuario.getName()
   

def comprobarExistenciaUsuario(usuario):
    try:
        usuarioObtenido = Users.get(Users.username == usuario)
        return True
    except:
        return False

def comprobarUsuario(usuario):
    md5 = hashlib.md5()
    md5.update(usuario.getPassword().encode('utf-8'))
    newPassword = md5.hexdigest()
    try:
        query = (Users.select().where( (Users.username == usuario.getName()) & (Users.password == newPassword) ).get() )
        return True
    except Exception as e:
        return False

def buscarEnListaDePartidas(usuario):
    try:
        listaObtenida = Listapartida.get(Listapartida.username == usuario)
        return True
    except:
        return False

def crearListaUsuario(usuario):
    try:
        with database.atomic():
            lista = Listapartida.create(idpartida=None, partidasganadas=0, partidastotales=0, username=usuario)
            lista.save()
        return True
    except peewee.IntegrityError:
        return 'Error: %s No se pudo crear la lista de partidas del usuario'

def actualizar(usuario,resultado):
    try:
        if resultado == True:
            with database.atomic():
                query = Listapartida.update(partidasganadas=Listapartida.partidasganadas +1).where(Listapartida.username == usuario)
                query.execute()
            with database.atomic():
                query = Listapartida.update(partidastotales=Listapartida.partidastotales +1).where(Listapartida.username == usuario)
                query.execute()
            return True
        else:
            with database.atomic():
                query = Listapartida.update(partidastotales=Listapartida.partidastotales +1).where(Listapartida.username == usuario)
                query.execute()
            return True
    except peewee.IntegrityError:
        return 'Error %s No se pudo actualizar la lista de partidas del usuario'

def obtenerMejoresJugadores():
    lista = []
    try:
        for x in listapartida.select().order_by(-listapartida.partidasganadas):
            lista.append(x)
        return lista
    except e:
        return 'Error en la obtencion de los jugadores'
