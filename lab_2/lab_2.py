import os
import sys
from random import randint as rd
#Корpеляция - ковариация деленная на произведение стандартных отклонений переменных

def write_file_with_binary_mode(filename: str, list_of_bytes: list):
    with open(f'{filename}', 'wb') as write_file:
        write_file.write(bytes(list_of_bytes))

def read_file_with_binary_mode(filename: str):
    with open(f'{filename}', "rb") as read_file:
        binary = read_file.read()
    return [i for i in binary]

def get_random_digit():
    return rd(0, 255)

def open_file_in_system(filename: str, flag):
    if flag:
        os.system(f'xdg-open {filename}')
    else:
        print("Access denied!")
        sys.exit()

def generate_key(list_of_bytes: list):
    key = [get_random_digit() for i in list_of_bytes]
    with open('key.txt', 'w') as write_file:
        for i in key:
            write_file.write(f"{i} ")

def encryption(filename: str):# гаммирование
    list_of_bytes = read_file_with_binary_mode(filename)
    generate_key(list_of_bytes)
    with open('key.txt', 'r') as read_file:
        key = read_file.read().split()
    return [(list_of_bytes[i] ^ int(key[i])) for i in range(len(list_of_bytes))]


def decryption(list_of_bytes: list):
    with open('key.txt', 'r') as read_file:
        key = read_file.read().split()
    return [(list_of_bytes[i] ^ int(key[i])) for i in range(len(list_of_bytes))]

def check_password(password: str):
    with open ('password.txt', 'r') as read_file:
        password_from_file = read_file.read()
    if password == password_from_file:
        return True
    else:
        return False

def main():
    filename = input("enter filename: ")
    question = input("do you want encryption file? y/n: ")
    if question == 'y':
        list_enc = encryption(filename)
        write_file_with_binary_mode(f"enc/{filename}", list_enc)
        password = input('enter password for decryption: ')
        if check_password(password):
            list_dec = decryption(list_enc)
            write_file_with_binary_mode(f"dec/{filename}",list_dec)
            open_file_in_system(f"dec/{filename}", True)
            sys.exit()
        else:
            print("password if wrong! ")
            sys.exit()

    elif question == 'n':
        open_file_in_system(filename, True)
        sys.exit()
    else:
        print("Incorrect input!!!")
        sys.exit()

if __name__ == "__main__":
    main()