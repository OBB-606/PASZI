import hashlib

login = "ADMIN".encode()
password = '1234'.encode()

dk = hashlib.pbkdf2_hmac('sha256', login, password, 100000)
rock = dk.hex()
print(rock)
with open('/media/valery/JOKER/certificate.txt', 'w') as write_file:
    write_file.write(f"{rock}")


with open('/media/valery/JOKER/certificate.txt', 'r') as read_file:
    tmp = read_file.read()

if tmp == str(rock):
    print('hui')