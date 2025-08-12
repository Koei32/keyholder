# list - lists stored passwords
# view - view a password
# new - create a new password
# edit -
# delete -

from password_mgt import *
import time
from console import print
from rich import table
from password_mgt import get_password, get_title
from dataproc import *


def new_password():
    try:
        title = get_title()
        pwd = get_password("Enter new password: ", confirm=True)
        notes = input("Notes (optional): ")

        master_pwd = get_password("Enter your master password: ")
        while not auth(master_pwd):
            print("Password is wrong! Try again.")
            master_pwd = get_password("Enter your master password: ")

        with open("./data.dat", "rb") as f:
            if len(f.read()) == 0:
                # this is the first password to be stored
                id = 1
                password_obj = {id: (title, pwd, notes)}
                new_pwd_data = encrypt_data(password_obj, master_pwd)
            else:
                stored_data = decrypt_data(load_data(), master_pwd)
                id = list(stored_data.keys())[-1] + 1
                password_obj = {id: (title, pwd, notes)}
                stored_data.update(password_obj)
                new_pwd_data = encrypt_data(stored_data, master_pwd)
        write_data(new_pwd_data)
    except KeyboardInterrupt:
        print("Cancelled new password creation.")

def view():
    master_pwd = get_password("Master password: ")
    if auth(master_pwd):
        pwd_data = decrypt_data(load_data(), master_pwd)
        print(pwd_data)
    else:
        print("")


def first_boot():
    print(
        "\nWelcome to [bold violet]Keyholder[/bold violet]. This is your first boot of the app. Set a [bold]master password[/bold] to continue.\n"
    )
    time.sleep(0.5)
    print(
        "\nYou will be using this password to access all of your other stored passwords."
    )
    time.sleep(2)
    print(
        "Please make sure that the password you select is strong, unique and memorable."
    )
    time.sleep(2)
    print(
        "!! [bold red]If you forget the master password, there is NO way to retrieve your stored passwords.[/bold red] !!"
    )
    time.sleep(2)
    set_master_password()
    datafile = open("./data.dat", "w").close()

CMD_LIST = {
    "new": new_password,
    "view": view,
}