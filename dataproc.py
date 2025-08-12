import pickle
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac
from base64 import urlsafe_b64encode, urlsafe_b64decode, encode, decode
import base64



def load_data() -> bytes:
    # load all dicts from data file(s)
    with open("./data.dat", "+rb") as f:
        pdata = f.read()
    return pdata


def write_data(data: bytes):
    # writes `data` to datafile
    with open("./data.dat", "+wb") as f:
        f.write(data)


def decrypt_data(data: bytes, master_pwd: str) -> dict:
    """
    Decrypts `data` with a key derived from `master_pwd` using pbkdf2.
    ### Returns:
    `bytes` object containing decrypted data.
    """
    with open("pwd.dat", "rb") as f:
        master_key = pbkdf2_hmac("sha256", master_pwd.encode(), pickle.load(f)[1], 1_200_000)
    fernet = Fernet(urlsafe_b64encode(master_key))
    pdata: dict = pickle.loads(fernet.decrypt(data))
    return pdata


def encrypt_data(data: dict, master_pwd: str) -> bytes:
    """
    Encrypts `data` with a key derived from `master_pwd` using pbkdf2.
    ### Returns:
    `bytes` object containing encrypted data.
    """

    with open("./pwd.dat", "rb") as f:
        master_key = pbkdf2_hmac("sha256", master_pwd.encode(), pickle.load(f)[1], 1_200_000)
    fernet = Fernet(urlsafe_b64encode(master_key))  # encrypts `data` with `key`
    pickled = pickle.dumps(data)  # returns pickled dict
    enc_data = fernet.encrypt(pickled)
    return enc_data
