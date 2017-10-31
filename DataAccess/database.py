from peewee import *
#import _mysql

from BusinessLogic.Usuario import Usuario

#db = _mysql.connect(host="localhost",)
db = MySQLDatabase(host='localhost',user='root', passwd='narval93',database='buscaminas.db')


class User(Model):
    __username = CharField(unique=True)
    __password = CharField()

    class Meta:
        database = db

    def crearUsuario(Usuario):
        user = User.create(username = Usuario.getName(),password = Usuario.getPassword())
        db.connect()

def before_request_handler():
    db.connect()

def after_request_handler():
    db.close()






