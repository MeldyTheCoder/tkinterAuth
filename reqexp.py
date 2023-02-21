import re

class RegExp:
    def __init__(self):
        self.__login_pattern = "[a-z]?(.|\-)+(\w+|\b)"

    def check_login(self, login: str):
        return re.match(self.__login_pattern, login)