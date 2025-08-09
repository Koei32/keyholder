from getpass import getpass
import os
import pickle
from hashlib import pbkdf2_hmac, sha256
from secrets import compare_digest

def get_password():
    pwd = getpass("Password: ")
    return pwd

def set_master_password(pwd):
    sha = sha256()
    salt = os.urandom(16)
    sha.update(pwd+salt)
    final_hash = sha.hexdigest()
    pwd_data = [final_hash, salt]
    with open("pwd.dat", "wb") as f:
        pickle.dump(pwd_data, f)

def auth(pwd):
    with open("pwd.dat", "rb") as f:
        pwd_data = pickle.load(f)
    sha = sha256()
    sha.update(pwd+pwd_data[1])
    pwd_hash = sha.hexdigest()
    return compare_digest(pwd_data[0], pwd_hash)
    
