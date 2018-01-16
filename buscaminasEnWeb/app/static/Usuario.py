class Usuario:
    def __init__(self, name, password,email):
        self.__name = name
        self.__password = password
        self.__email = email

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password

    def get_email(self):
        return self.__email