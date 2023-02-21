import hashlib
import hmac
from typing import Union
from database import Database
from reqexp import RegExp

rg = RegExp()

class Authorization:
    def __init__(self, db: Database):
        self.db = db
        self.alg = hashlib.sha256
        self.encoding = 'ascii'
        self.__secret = "some_secret"

    def __generate_hmac(self, secret: Union[str, bytes], data: Union[str, bytes]):
        if isinstance(secret, str):
            secret = bytes(secret, self.encoding)

        if isinstance(data, str):
            data = bytes(data, self.encoding)

        return hmac.new(secret, data, digestmod=self.alg).hexdigest()

    def __check_hmac(self, secret: Union[str, bytes], password: Union[str, bytes], hash: Union[str, bytes]):
        new_hmac = self.__generate_hmac(secret, password)
        return hmac.compare_digest(new_hmac, hash)

    def registration(self, login: str, password: str):
        if not rg.check_login(login):
            raise Exception("Некорректно введен логин!")

        elif self.db.get_user(login=login):
            raise Exception("Пользователь с таким логином уже существует!")

        key = self.__generate_hmac(self.__secret, password)
        self.db.add_user(login=login, password=key)

    def authorize(self, login: str, password: str):
        user_data = self.db.get_user(login=login)
        if not user_data:
            raise Exception("Пользователя не существует")

        check = self.__check_hmac(self.__secret, password, user_data["password"])
        if not check:
            raise Exception("Неверный пароль")

