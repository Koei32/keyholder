import pickle
from cryptography.fernet import Fernet
from hashlib import pbkdf2_hmac


def load_data() -> tuple:
    # load all dicts from data file(s)
    with open("./data.dat", "rb") as f:
        pdata = tuple(pickle.load(f))
    return pdata


def write_data(data: tuple):
    # writes `data` to datafile
    with open("./data.dat", "+wb") as f:
        pickle.dump(data, f)


def decrypt_data(data: bytes, master_pwd: bytes) -> tuple:
    """
    Decrypts `data` with a key derived from `master_pwd` using pbkdf2.
    ### Returns:
    `bytes` object containing decrypted data.
    """

    with open("pwd.data", "rb") as f:
        master_key = pbkdf2_hmac("sha256", master_pwd, pickle.load(f)[1], 1_200_000)

    fernet = Fernet(master_key)
    pdata = pickle.loads(fernet.decrypt(data))
    return pdata


def encrypt_data(data: tuple, master_pwd: bytes) -> bytes:
    """
    Encrypts `data` with a key derived from `master_pwd` using pbkdf2.
    ### Returns:
    `bytes` object containing encrypted data.
    """

    with open("pwd.data", "rb") as f:
        master_key = pbkdf2_hmac("sha256", master_pwd, pickle.load(f)[1], 1_200_000)
    fernet = Fernet(master_key)  # encrypts `data` with `key`
    pickled = pickle.dumps(data)  # returns pickled tuple of dicts
    enc_data = fernet.encrypt(pickled)
    return enc_data
