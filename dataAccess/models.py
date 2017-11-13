#! /usr/bin/env python35
import peewee

database = peewee.MySQLDatabase('buscaminas', **{'user': 'root', 'password': 'narval93'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(peewee.Model):
    class Meta:
        database = database

class Users(BaseModel):
    password = peewee.CharField(null=True)
    username = peewee.CharField(primary_key=True)

    class Meta:
        db_table = 'users'

def crearUsuario(Usuario):
    user = Users.create(username = Usuario.getName(), password= Usuario.getPassword())
    user.save()