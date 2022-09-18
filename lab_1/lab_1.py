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
import sys
from functools import partial
import json
import tkinter as tk
import re
from tkinter import messagebox
counter = 0
with open ('block.json', 'r') as read_file:
    dict_block = json.load(read_file)
def check_certificate(window):
    with open('/media/valery/JOKER/certificate.txt', 'r') as read_file:
        certificate = read_file.read()
    check = True
    for i in dict_of_user_information:
        l = i.encode()
        p = dict_of_user_information[i].encode()
        dk = hashlib.pbkdf2_hmac('sha256', l, p, 100000)
        hash_ = dk.hex()
        if str(hash_) == certificate:
            check = True
        else:
            check = False
        if check is False:
            messagebox.showinfo("Error", "У вас некорректные сертификат")
        else:
            accounting([i, dict_of_user_information[i], window])
            break
def delete_user(login):
    try:
        global dict_of_user_information
        dict_of_user_information.pop(login.get())
        write_json_file('db.json')
        dict_of_user_information = read_json_file('db.json')
    except KeyError:
        print('Неверный ключ')
def check_correct_password(lst: list):
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[а-я].*)(?=.*[А-Я].*)[0-9a-zA-Zа-яА-Я$%#^]{8,}$')
    password = lst[2].get()
    print(password)
    if bool(pattern_password.match(password)):
        if lst[0] == "ADMIN":
            register_admin(lst)
        else:
            register_user(lst)
    else:
        messagebox.showinfo("Error", "Пароль не соответствует требованиям!")



def read_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}') as read_file:
        return json.load(read_file)

dict_of_user_information = read_json_file('db.json')
dict_of_user_information['ADMIN'] = '1234'

def write_json_file(filename: str):
    global dict_of_user_information
    with open(f'{filename}', 'w') as write_file:
        json.dump(dict_of_user_information, write_file, indent=3)

write_json_file('db.json')

def block_or_nonblock(lst: list):
    with open('block.json', "w") as write_file:
        if lst[1] is True:
            dict_block[lst[0].get()] = True
        else:
            dict_block[lst[0].get()] = False
        json.dump(dict_block, write_file, indent=3)

def get_information(lst: list):
    global dict_of_user_information
    dict_of_user_information = read_json_file('db.json')
    s = ""
    for i in dict_of_user_information:
        s += f"{i} -- {dict_of_user_information[i]} -- block: {dict_block[i]}\n"
    lst[1].insert(1.0, s)
    s = ""
def register_admin(lst: list):
    global dict_of_user_information
    dict_of_user_information[lst[1].get()] = lst[2].get()
    write_json_file('db.json')

def register_user(lst: list):
    global dict_of_user_information
    dict_of_user_information[lst[1]] = lst[2].get()
    write_json_file('db.json')

def clear_textfield(textfield):
    textfield.delete(1.0, tk.END)
def new_accounting(current_window):
    current_window.destroy()
    main()

def accounting(lst: list):
    global dict_of_user_information, counter
    if type(lst[0]) is str:
        login = lst[0]
        password = lst[1]
    else:
        login = lst[0].get()
        password = lst[1].get()


    if dict_block[login] == False:
        messagebox.showinfo("Error", "Вам запрещен доступ!")
        lst[2].destroy()
        main()

    read_json_file('db.json')
    if login in dict_of_user_information.keys() and password in dict_of_user_information.values():
        if login == "ADMIN" and password == '1234':
            counter = 0
            lst[2].destroy()
            window_in_system_admin = tk.Tk()
            window_in_system_admin.geometry('400x700')
            window_in_system_admin.resizable(False, False)
            window_in_system_admin.title("ADMIN")
            label_admin_new_login = tk.Label(window_in_system_admin, text="Логин пользователя")
            label_admin_new_login.pack()
            entry_admin_new_login = tk.Entry(window_in_system_admin)
            entry_admin_new_login.pack()
            label_admin_new_password = tk.Label(window_in_system_admin, text="Пароль пользователя")
            label_admin_new_password.pack()
            entry_admin_new_password = tk.Entry(window_in_system_admin, show="*")
            entry_admin_new_password.pack()
            button_admin_register = tk.Button(window_in_system_admin, width=22, text="Сменить/ создать",
                                              command=partial(check_correct_password, [login, entry_admin_new_login, entry_admin_new_password]))
            button_block_admin = tk.Button(window_in_system_admin, width=22, text="Наложить ограничение", command=partial(block_or_nonblock, [entry_admin_new_login, False]))
            button_unblock_admin = tk.Button(window_in_system_admin, width=22, text="Снять ограниечение", command=partial(block_or_nonblock, [entry_admin_new_login, True]))


            button_admin_register.pack()

            button_block_admin.pack()
            button_unblock_admin.pack()

            button_delete_user = tk.Button(window_in_system_admin, width=22, text='Удалить пользователя',
                                           command=partial(delete_user, entry_admin_new_login))
            button_delete_user.pack()
            text_admin = tk.Text(width=40, height=15)


            button_get_information_about_users = tk.Button(window_in_system_admin, width=22, text="Получить информацию",
                                                           command=partial(get_information, [window_in_system_admin, text_admin]))
            button_get_information_about_users.pack()
            scroll = tk.Scrollbar(command=text_admin.yview)
            scroll.pack(side=tk.LEFT, fill=tk.Y)

            text_admin.config(yscrollcommand=scroll.set)

            text_admin.pack()

            button_clear_text_field = tk.Button(text="Очиcтить поле", width=22, command=partial(clear_textfield, text_admin))
            button_clear_text_field.pack()

            button_register = tk.Button(window_in_system_admin, width=22, text="Авторизоваться заново",
                                        command=partial(new_accounting, window_in_system_admin))
            button_register.pack()

            button_destroy = tk.Button(window_in_system_admin, width=22, text="Закончить работу!",
                                       command=window_in_system_admin.destroy)
            button_destroy.pack()

            window_in_system_admin.mainloop()
        elif (login, password) in list(dict_of_user_information.items()):
            counter = 0
            lst[2].destroy()

            window_in_system_user = tk.Tk()
            window_in_system_user.geometry("500x500")
            window_in_system_user.resizable(False, False)
            window_in_system_user.title(f"user {login}")
            label_user_new_login = tk.Label(window_in_system_user,
                                            text="Если есть желание, поменяйте свои данные для входа в систему")
            label_user_new_login.pack()
            label_user_new_password = tk.Label(window_in_system_user, text="Поменяйте пароль")
            label_user_new_password.pack()
            entry_user_new_password = tk.Entry(window_in_system_user, show="*")
            entry_user_new_password.pack()
            button_register_user = tk.Button(window_in_system_user, width=22, text="Send Data",
                                             command=partial(check_correct_password, [login, login, entry_user_new_password]))
            button_register_user.pack()
            button_destroy = tk.Button(window_in_system_user, width=22, text="Закончить работу!",
                                       command=window_in_system_user.destroy)
            button_destroy.pack()
            button_register = tk.Button(window_in_system_user, width=22, text="Авторизоваться заново",
                                        command=partial(new_accounting, window_in_system_user))
            button_register.pack()
            window_in_system_user.mainloop()

    else:
        counter +=1
        lst[2].destroy()
        if counter >=3:
            messagebox.showinfo('ERROR', 'У вас было слишком много попыток войти!')
            sys.exit()
        main()

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
    authorize_button = tk.Button(window, text="Authorization", width=22,
                                 command=partial(accounting, [entry_login, entry_password, window]))
    label.pack()
    label_login.pack()
    entry_login.pack()
    label_password.pack()
    entry_password.pack()
    authorize_button.pack()
    certificate_button = tk.Button(text="check_certificate", width=22, command=partial(check_certificate, window))
    certificate_button.pack()
    window.mainloop()

main()
