import re
from re import findall




template = r"[a-zA-Zа-яА-Я0-9\+\-\*\/\$\!\@]"
a = findall(template, "Rock123абВ!-/")
print(a)