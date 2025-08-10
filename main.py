from dataproc import *
from password_mgt import *
from rich import print
from pathlib import Path
from commands import first_boot

pwd_file = Path("./pwd.dat")
data_file = Path("./data.dat")

def main():
    
    
    # normal program loop here
    pwd = getpass()
    print(auth(pwd))
    




    # salt = b'c2lua3BhZ2Vjb21wbGV4aQ=='
    # data = load_data()
    # master = input("password: ").encode()
    # kdf = PBKDF2HMAC(hashes.SHA256(), length=32, salt=salt, iterations=1_200_000)
    # key = base64.urlsafe_b64encode(kdf.derive(master))
    # data = decrypt_data(bytes(data), key)

def test(id):
    t = input("Title: ")
    p = getpass()
    c = input("Comments: ")
    titles[id], hash[id], comments[id] = t, p, c



if __name__ == "__main__":
    titles, hash, comments = dict(), dict(), dict()
    
    if not pwd_file.is_file() and not data_file.is_file():
        # if we are here, this is the first run of the program
        first_boot()
    
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Quitting...")

