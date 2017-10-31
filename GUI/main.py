from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.config import Config
from kivy.properties import StringProperty
from kivy.lang import Observable
from os.path import join, dirname
import gettext
import BusinessLogic.internationalization
import sys
sys.path.insert(0, '/BusinessLogic/DataAccess/database')
#import database
from DataAccess.database import User
from BusinessLogic.Usuario import Usuario
Window.size = (300, 500)

class ScreenManagement(ScreenManager):
    pass

class Buscaminas(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Buscaminas, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Buscaminas, self).fbind(name, func, args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Buscaminas, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('buscaminasapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)
    pass

class LoginScreen(Screen):
    pass

class Usuario_BaseDeDatos(User):
    pass


class RegistroScreen(Screen):
    def check_label(self, username,password):
        if(username != "" and password !=""):
            user = Usuario(username,password)
            Usuario_BaseDeDatos.crearUsuario(user)

            print(user.getName())
            print(user.getPassword())
        else:
            #mostrar ventana de que debe introducir clave
            print("no")
    pass

class MenuScreen(Screen):
    pass

class Menu2Screen(Screen):
    pass

class IdiomaScreen(Screen):
    pass

class Tablero1(Screen):
    pass


tr = Buscaminas("en")

class BuscaminasApp(App):
    login = StringProperty('en')

    def on_login(self, instance, login):
        tr.switch_lang(login)





if __name__ == "__main__":
    #initial_db()
    BuscaminasApp().run()