from tkinter import Tk, Label, Entry, Button, Frame, messagebox, W, StringVar
from authorization import Authorization
from database import Database
from abc import abstractmethod

db = Database("db.sqlite")
auth = Authorization(db)

class BaseActivity:
    title = "BaseActivity"

    def __init__(self, root: Tk = None):
        self.root = root if root else Tk()
        self.root.title("Авторизация")
        self.frame = Frame(self.root, padx=10, pady=10)
        self.frame.pack()
        self._on_start()

    @abstractmethod
    def _on_start(self):
        print("Виджеты не добавлены!")

    @abstractmethod
    def _on_activity_change(self):
        pass

    def mainloop(self, **kwargs):
        return self.root.mainloop(**kwargs)

    def setActivity(self, activity):
        if not issubclass(activity, BaseActivity):
            raise Exception('Not an activity!')
        self._on_activity_change()
        new_activity = activity(self.root)
        return new_activity

class LoginActivity(BaseActivity):
    title = "Авторизация"

    def __login(self):
        login = self.username.get()
        password = self.password.get()
        if not password or not login:
            return messagebox.showerror("Ошибка!", "Не все поля заполнены!")
        try:
            auth.authorize(login, password)
            return messagebox.showinfo("Успех!", "Вы успешно зашли!")
        except Exception as e:
            return messagebox.showerror("Ошибка!", e)


    def _on_start(self):
        self.head = Label(self.root, text=self.title, font=("", 35), pady=10)
        self.head.pack()
        self.username = StringVar()
        self.password = StringVar()
        Label(self.frame, text="Логин: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.frame, textvariable=self.username, bd=5, font=("", 15)).grid(row=0, column=1)
        Label(self.frame, text="Пароль: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.frame, textvariable=self.password, bd=5, font=("", 15), show="*").grid(row=1, column=1)
        Button(self.frame, text="Войти", bd=3, font=("", 15), padx=5, pady=5, command=self.__login).grid()
        Button(self.frame, text="Регистрация", bd=3, font=("", 15), padx=5, pady=5, command=lambda *args: self.setActivity(RegisterActivity)).grid()

    def _on_activity_change(self):
        self.head.pack_forget()
        self.username.set("")
        self.password.set("")
        self.frame.pack_forget()


class RegisterActivity(BaseActivity):
    title = "Регистрация"

    def __register(self):
        username = self.username.get()
        password = self.password.get()
        if not password or not username:
            return messagebox.showerror("Ошибка!", "Не все поля заполнены!")

        try:
            auth.registration(username, password)
            return messagebox.showinfo("Успех!", "Вы успешно зарегистрировались")
        except Exception as e:
            return messagebox.showerror("Ошибка!", e)

    def _on_start(self):
        self.head = Label(self.root, text=self.title, font=("", 35), pady=10)
        self.head.pack()
        self.username = StringVar()
        self.password = StringVar()
        Label(self.frame, text="Логин: ", font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.frame, textvariable=self.username, bd=5, font=("", 15)).grid(row=0, column=1)
        Label(self.frame, text='Пароль: ', font=("", 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.frame, textvariable=self.password, bd=5, font=("", 15), show="*").grid(row=1, column=1)
        Button(self.frame, text="Зарегистрироваться", bd=3, font=("", 15), padx=5, pady=5, command=self.__register).grid()
        Button(self.frame, text='Назад', bd=3, font=("", 15), padx=5, pady=5, command=lambda *args: self.setActivity(LoginActivity)).grid()

    def _on_activity_change(self):
        self.head.pack_forget()
        self.username.set("")
        self.password.set("")
        self.frame.pack_forget()




