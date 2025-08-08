from functions import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import base64
import hashlib
from string import ascii_letters
import secrets

# PLEASE CLEAN THIS UP
def main():
    salt = b'c2lua3BhZ2Vjb21wbGV4aQ=='
    data = load_data()
    master = input("password").encode()
    kdf = PBKDF2HMAC(hashes.SHA256(), length=32, salt=salt, iterations=1_200_000)
    key = base64.urlsafe_b64encode(kdf.derive(master))

    data = decrypt_data(bytes(data), key)
    print(data[0])
    print(data[1])
    print(data[2])
    # return
    master = b"this"
    kdf = PBKDF2HMAC(hashes.SHA256(), length=32, salt=salt, iterations=1_200_000)
    key = base64.urlsafe_b64encode(kdf.derive(master))
    master = None
    for id in range(2):
        test(id)
    data = encrypt_data((titles, hash, comments), key)
    write_data(data)
    data = None
    data = load_data()
    master = input("password").encode()
    kdf = PBKDF2HMAC(hashes.SHA256(), length=32, salt=salt, iterations=1_200_000)
    key = base64.urlsafe_b64encode(kdf.derive(master))

    data = decrypt_data(bytes(data), key)
    print(data[0])
    print(data[1])
    print(data[2])


def test(id):
    t = input("Title: ")
    p = get_password()
    c = input("Comments: ")
    titles[id], hash[id], comments[id] = t, p, c

if __name__ == "__main__":
    titles, hash, comments = dict(), dict(), dict()
    main()

