#! /usr/bin/env python35
from peewee import *
import hashlib

database = MySQLDatabase('buscaminas', **{'password': 'qwertyasd', 'user': 'admin'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    password = CharField()
    username = CharField(primary_key=True)

    class Meta:
        db_table = 'users'

class Listapartida(BaseModel):
    idlista = PrimaryKeyField(db_column='idLista')
    partidasganadas = IntegerField(db_column='partidasGanadas', null=True)
    partidastotales = IntegerField(db_column='partidasTotales', null=True)
    username = ForeignKeyField(db_column='username', rel_model=Users, to_field='username')

    class Meta:
        db_table = 'listapartida'

def crearUsuario(Usuario):
        try:
            with database.atomic():
                md5 = hashlib.md5()
                md5.update(Usuario.getPassword().encode('utf-8'))
                newPassword = md5.hexdigest()
                user = Users.create(username = Usuario.getName(), password = newPassword)
                user.save()
            return True
        except peewee.IngrityError:
            return 'Error: %s No se pudo crear el usuario ' % Usuario.getName()
   

def comprobarUsuario(usuario):
    try:
        usuarioObtenido = Users.get(Users.username == usuario)
        return True
    except:
        return False

