class Usuario:
    def __init__(self, name, password,email):
        self.__name = name
        self.__password = password
        self.__email = email

    def getName(self):
        return self.__name

    def getPassword(self):
        return self.__password

    def getEmail(self):
        return self.__email