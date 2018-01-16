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
                md5.update(Usuario.get_password().encode('utf-8'))
                newPassword = md5.hexdigest()
                user = Users.create(username = Usuario.get_name(), password = newPassword, email = Usuario.get_email())
                user.save()
            return True
        except peewee.IntegrityError:
            return 'Error: %s No se pudo crear el usuario ' % Usuario.get_name()
   

def comprobarExistenciaUsuario(usuario):
    try:
        usuarioObtenido = Users.get(Users.username == usuario)
        return True
    except:
        return False

def comprobarUsuario(usuario):
    md5 = hashlib.md5()
    md5.update(usuario.get_password().encode('utf-8'))
    newPassword = md5.hexdigest()
    try:
        query = (Users.select().where( (Users.username == usuario.get_name()) & (Users.password == newPassword) ).get() )
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
        user = Users.get()
        partida = Listapartida.get()
        sq = Listapartida.select().order_by(Listapartida.partidasganadas.desc())
        toppings = list(sq)
        usuarios = Listapartida.select().join(Users).order_by(Listapartida.partidasganadas.desc())
        print(usuarios)

        for us in usuarios:
            us.user.partida
            numPartidas = us.partidasganadas
            query = Listapartida.select(Listapartida.username).where (partidasganadas == numPartidas)
            print(query.execute())

    except:
        return 'Error en la obtencion de los jugadores'

def obtenerPerfilUsuario(usuario):
    try:
        usuarioObtenido = Users.get(Users.username == usuario)
        user = Usuario(usuarioObtenido.username,"",usuarioObtenido.email)
        return user
    except:
        return 'no se puede obtener el usuario'