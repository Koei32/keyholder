# view - view a password
# new - create a new password
# edit -
# delete -

from password_mgt import *
import time
from console import print
from rich.table import Table
from password_mgt import get_password, get_title
from dataproc import *
from rich import box

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

def list_passwords():
    master_pwd = get_password("Master password: ")
    if not auth(master_pwd):
        print("Invalid password")
        return
    pwd_data = decrypt_data(load_data(), master_pwd)
    table = Table(title="Stored passwords")
    table.add_column("id", style="white")
    table.add_column("title", style="cyan")
    table.add_column("password", style="green italic")
    table.add_column("notes", style="white")

    for i in range(len(pwd_data)):
        # lord forgive me
        table.add_row(str(list(pwd_data.keys())[i])+".", list(pwd_data.values())[i][0], list(pwd_data.values())[i][1], list(pwd_data.values())[i][2])
    print(table)


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


def showhelp():
    print("\nHere are the available commands:")
    table = Table(box=box.MINIMAL_DOUBLE_HEAD, show_lines=True)
    table.add_column("command")
    table.add_column("description")
    for x in range(len(CMD_HELP)):
        table.add_row(list(CMD_HELP.keys())[x], list(CMD_HELP.values())[x])
    print(table)

# 1. new  : store a new password
# 2. view : view your stored passwords (this is barebones and insecure for now)
# 3. help : view this help message

# CMD_HELP = [
#     "new : Store a new password. Asks for a title (e.g. name of a site or service), password and optional notes.",
#     "list : Lists stored passwords. Doesnt display the actual password. (see '[bold]view[/bold]') ",
#     "view <id/title> : View a password in plaintext using its id or title. (e.g. view 3 or view )",
#     "help : Displays this help message."
# ]
CMD_HELP = {
    "new" : "Store a new password. Asks for a title (e.g. name of a site or service), password and optional notes.",
    "list" : "Lists stored passwords. Doesnt display the actual password. (see '[bold]view[/bold]') ",
    "view <id/title>" : "View a password in plaintext using its id or title. (e.g. view 3 or view )",
    "help" : "Displays this help message."
}

CMD_LIST = {
    "new": new_password,
    "list": list_passwords,
    "help": showhelp
}