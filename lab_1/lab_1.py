'''
Система авторизации с GUI.
2 режима: admin и user

В режиме админа:
    смена пароля админа
    просмотр списка зарегистрированных пользователей
    возможность редактировать файл с пользователями
    завершение работы программы

В режиме пользователя:
    менять пароль текущего пользователя
    завершение работы с программой

Должно быть реализовано окно авторизации, где символы пароля заменяются '*'. В этом же окне
должна быть функция авторизации с помощью сертификата, который находится на флешке. Сертификат может
представлять из себя текстовый документ, в котором содержится хеш сконкатенированных логина и пароля.

'''
import hashlib
from functools import partial
import json
import tkinter as tk
from tkinter import messagebox

def check_certificate(window):
    with open('/media/valery/JOKER/certificate.txt', 'r') as read_file:
        certificate = read_file.read()

    for i in dict_of_user_information:
        l = i.encode()
        p = dict_of_user_information[i].encode()
        dk = hashlib.pbkdf2_hmac('sha256', l, p, 100000)
        hash_ = dk.hex()
        if str(hash_) == certificate:
            accounting([i, dict_of_user_information[i], window])

def read_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}') as read_file:
        return json.load(read_file)

dict_of_user_information = read_json_file('db.json')
dict_of_user_information['ADMIN'] = '1234'

def write_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}', 'w') as write_file:
        json.dump(dict_of_user_information, write_file)

write_json_file('db.json')

def get_information(current_window):
    global dict_of_user_information
    dict_of_user_information = read_json_file('db.json')
    label_information = tk.Label(current_window, text=f'{dict_of_user_information}').pack()

def register_admin(lst: list):
    global dict_of_user_information
    dict_of_user_information[lst[0].get()] = lst[1].get()
    write_json_file('db.json')

def register_user(lst: list):
    global dict_of_user_information
    dict_of_user_information[lst[0]] = lst[1].get()
    write_json_file('db.json')

def new_accounting(current_window):
    current_window.destroy()
    main()

def accounting(lst: list):
    global dict_of_user_information
    if type(lst[0]) is str:
        login = lst[0]
        password = lst[1]
    else:
        login = lst[0].get()
        password = lst[1].get()
    read_json_file('db.json')
    if login in dict_of_user_information.keys():
        if login == "ADMIN" and password == '1234':
            lst[2].destroy()
            messagebox.showinfo('ROCK!', 'Rock!!!!')
            window_in_system_admin = tk.Tk()
            window_in_system_admin.geometry('300x500')
            window_in_system_admin.resizable(False, False)
            window_in_system_admin.title("ADMIN")
            label_admin_new_login = tk.Label(window_in_system_admin, text="Введите новый логин пользователя")
            label_admin_new_login.pack()
            entry_admin_new_login = tk.Entry(window_in_system_admin)
            entry_admin_new_login.pack()
            label_admin_new_password = tk.Label(window_in_system_admin, text="Введите новый пароль пользователя")
            label_admin_new_password.pack()
            entry_admin_new_password = tk.Entry(window_in_system_admin, show="*")
            entry_admin_new_password.pack()
            button_admin_register = tk.Button(window_in_system_admin, text="Send Data",
                                              command=partial(register_admin, [entry_admin_new_login, entry_admin_new_password]))
            button_admin_register.pack()
            button_destroy = tk.Button(window_in_system_admin, text="Закончить работу!",
                                       command=window_in_system_admin.destroy)
            button_destroy.pack()
            button_register = tk.Button(window_in_system_admin, text="Авторизоваться заново",
                                        command=partial(new_accounting, window_in_system_admin))
            button_register.pack()
            button_get_information_about_users = tk.Button(window_in_system_admin, text="get_information",
                                                           command=partial(get_information, window_in_system_admin))
            button_get_information_about_users.pack()

            window_in_system_admin.mainloop()
        else:
            lst[2].destroy()
            messagebox.showinfo(f'USER', f'login: {login}, password: {password}')
            window_in_system_user = tk.Tk()
            window_in_system_user.geometry("500x500")
            window_in_system_user.resizable(False, False)
            window_in_system_user.title("user")
            label_user_new_login = tk.Label(window_in_system_user,
                                            text="Если есть желание, поменяйте свои данные для входа в систему")
            label_user_new_login.pack()
            label_user_new_password = tk.Label(window_in_system_user, text="Поменяйте пароль")
            label_user_new_password.pack()
            entry_user_new_password = tk.Entry(window_in_system_user, show="*")
            entry_user_new_password.pack()
            button_register_user = tk.Button(window_in_system_user, text="Send Data",
                                             command=partial(register_user, [login, entry_user_new_password]))
            button_register_user.pack()
            button_destroy = tk.Button(window_in_system_user, text="Закончить работу!",
                                       command=window_in_system_user.destroy)
            button_destroy.pack()
            button_register = tk.Button(window_in_system_user, text="Авторизоваться заново",
                                        command=partial(new_accounting, window_in_system_user))
            button_register.pack()
            window_in_system_user.mainloop()

    else:
        lst[2].destroy()
        messagebox.showinfo('Access denied!', 'НЕ РОК')


def main():
    window = tk.Tk()
    window.title("Accounting")
    window.geometry('200x200')
    window.resizable(False, False)
    label_login = tk.Label(text='login: ')
    label = tk.Label(text='Надо авторизоваться!')
    label_password = tk.Label(text='password: ')
    entry_login = tk.Entry()
    entry_password = tk.Entry(show='*')
    authorize_button = tk.Button(window, text="Authorization",
                                 command=partial(accounting, [entry_login, entry_password, window]))
    label.pack()
    label_login.pack()
    entry_login.pack()
    label_password.pack()
    entry_password.pack()
    authorize_button.pack()
    certificate_button = tk.Button(text="check_certificate", command=partial(check_certificate, window))
    certificate_button.pack()
    window.mainloop()

main()
