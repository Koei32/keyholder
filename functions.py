from getpass import getpass
import pickle
from cryptography.fernet import Fernet

def get_password():
    pwd = getpass("Password: ")
    return pwd


def load_data() -> tuple:
    #load all dicts from data file(s)
    with open("./data.dat", "rb") as f:
        pdata = tuple(pickle.load(f))
    return pdata

def write_data(data: bytes):
    #writes `data` to datafile
    with open("./data.dat", "+wb") as f:
        pickle.dump(data, f)

def decrypt_data(data: bytes, master_key: bytes) -> tuple:
    #decrypts `data` with `key`
    fernet = Fernet(master_key)
    pdata = pickle.loads(fernet.decrypt(data))
    return pdata

def encrypt_data(data: tuple, master_key: bytes) -> bytes:
    fernet = Fernet(master_key) #encrypts `data` with `key`
    pickled = pickle.dumps(data) #returns pickled tuple of dicts
    enc_data = fernet.encrypt(pickled)
    return enc_data

