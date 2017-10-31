class Usuario:
    def __init__(self, name, password):
        self.__name = name
        self.__password = password

    def getName(self):
        return self.__name

    def getPassword(self):
        return self.__password