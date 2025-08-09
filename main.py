from dataproc import *
from password_mgt import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich import print
from pathlib import Path
import os


datafile = Path("./data.dt")

# PLEASE CLEAN THIS UP
def main():
    if not datafile.is_file():
        # if we are here, this is the first run of the program
        print("Welcome to [bold violet]Keyholder[/bold violet]. This is your first boot of the app. Set a [bold]master password[/bold] to continue.\n")
        print("Please make sure that the password you select is strong, unique and memorable.")
        print("!! [bold red]If you forget the master password, there is NO way to retrieve your stored passwords.[/bold red] !!")
        pwd = getpass()
        set_master_password(pwd)




    # salt = b'c2lua3BhZ2Vjb21wbGV4aQ=='
    # data = load_data()
    # master = input("password: ").encode()
    # kdf = PBKDF2HMAC(hashes.SHA256(), length=32, salt=salt, iterations=1_200_000)
    # key = base64.urlsafe_b64encode(kdf.derive(master))
    # data = decrypt_data(bytes(data), key)

def test(id):
    t = input("Title: ")
    p = get_password()
    c = input("Comments: ")
    titles[id], hash[id], comments[id] = t, p, c

if __name__ == "__main__":
    titles, hash, comments = dict(), dict(), dict()
    main()

