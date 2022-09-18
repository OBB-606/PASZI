import re
import os


pattern_password = re.compile(
    r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)(?=.*[а-я].*)(?=.*[А-Я].*)[0-9a-zA-Zа-яА-Я$%#^]{8,}$')

password = ''
# password = input('write password: ')
print(bool(pattern_password.match(f'{password}')))
a = {}
for i in range(10):
    a[i] = (i**2)+i

s = ""

for i in a:
    s += f"{i} -- {a[i]}\n"

print(s)







#
# from tkinter import *
#
#
# def insert_text():
#     s = "Hello World"
#     text.insert(1.0, s)
#
#
# def get_text():
#     s = text.get(1.0, END)
#     label['text'] = s
#
#
# def delete_text():
#     text.delete(1.0, END)
#
#
# root = Tk()
#
# text = Text(width=25, height=5)
# text.pack()
#
# frame = Frame()
# frame.pack()
# Button(frame, text="Вставить",
#        command=insert_text).pack(side=LEFT)
# Button(frame, text="Взять",
#        command=get_text).pack(side=LEFT)
# Button(frame, text="Удалить",
#        command=delete_text).pack(side=LEFT)
#
# label = Label()
# label.pack()
#
# root.mainloop()