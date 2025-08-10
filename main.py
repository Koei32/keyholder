from dataproc import *
from password_mgt import *
from rich import print
from pathlib import Path
import time
import os


datafile = Path("./pwd.dat")

# PLEASE CLEAN THIS UP
def main():
    if not datafile.is_file():
        # if we are here, this is the first run of the program
        print("\nWelcome to [bold violet]Keyholder[/bold violet]. This is your first boot of the app. Set a [bold]master password[/bold] to continue.\n")
        time.sleep(0.5)
        print("\nYou will be using this password to access all of your other stored passwords.")
        time.sleep(2)
        print("Please make sure that the password you select is strong, unique and memorable.")
        time.sleep(2)
        print("!! [bold red]If you forget the master password, there is NO way to retrieve your stored passwords.[/bold red] !!")
        time.sleep(2)
        set_master_password()
        quit()
    
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
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Quitting...")

