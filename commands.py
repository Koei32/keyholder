from password_mgt import *
import time
from console import print, rule
from rich.table import Table
from password_mgt import get_password, get_title, valid_chars
from dataproc import *
from rich import box
import random


# view - view a password
# new - create a new password


def command_processor(cmd: str):
    if len(cmd.split()) > 1:
        CMD_LIST[cmd.split()[0]](cmd.split()[1])
    else:
        CMD_LIST[cmd]()


def login() -> bool:
    print("Log in to continue.")
    attempts = 3

    while attempts > 0:
        master_pwd = get_password("Master password: ")
        if auth(master_pwd):
            global MASTER
            MASTER = master_pwd
            return True
        else:
            print("Password is wrong!\n")
            attempts -= 1
    return False


def random_password(size):
    password = ""

    try:
        size = int(size)
    except ValueError:
        print("Please provide an int value.")
        return

    for i in range(size):
        password += random.choice(valid_chars)
    print(password)


def new_password():
    try:
        title = get_title()
        pwd = get_password("Enter new password: ", confirm=True)
        notes = input("Notes (optional): ")

        master_pwd = get_password("Enter your master password: ")
        while not auth(master_pwd):
            print("Password is wrong! Try again.")
            master_pwd = get_password("Enter your master password: ")

        with open(DATA_FILE, "rb") as f:
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


def view(*args):
    if len(args) == 0:
        print("[yellow]An id is required.[/yellow]")
        return
    id = args[0]


    master_pwd = get_password("Enter your master password: ")
    while not auth(master_pwd):
        print("Password is wrong! Try again.")
        master_pwd = get_password("Enter your master password: \r")
    stored_pwd_data = decrypt_data(load_data(), master_pwd)
    try:
        print("\nThe password will auto-clear after 20 seconds. (Press Ctrl+C to clear manually)")
        print("[bold green]" + stored_pwd_data[int(id)][1] + "[/]", end="\r")
        time.sleep(20)
        print(" "*(len(stored_pwd_data[int(id)][1]) + 1))
        return
    except KeyboardInterrupt:
        print(" "*(len(stored_pwd_data[int(id)][1]) + 1))
        return



#wip
def remove_password(id: int):
    master_pwd = get_password("Enter your master password: ")
    while not auth(master_pwd):
        print("Password is wrong! Try again.")
        master_pwd = get_password("Enter your master password: ")
    stored_pwd_data = decrypt_data(load_data(), master_pwd)


def list_passwords():
    if len(load_data()) == 0:
        print("[yellow]No passwords stored.[/yellow]")
        return
    # master_pwd = get_password("Master password: ")
    # if not auth(master_pwd):
    #     print("Invalid password")
    #     return
    pwd_data = decrypt_data(load_data(), MASTER)
    table = Table(title="Stored passwords")
    table.add_column("id", style="white")
    table.add_column("title", style="cyan")
    table.add_column("password", style="green italic")
    table.add_column("notes", style="white")

    for i in range(len(pwd_data)):
        # lord forgive me
        table.add_row(
            str(list(pwd_data.keys())[i]) + ".", list(pwd_data.values())[i][0], "********", list(pwd_data.values())[i][2],
        )
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
    datafile = open(DATA_FILE, "w").close()


def showhelp():
    print("\nHere are the available commands:")
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("command", style="green")
    table.add_column("description")
    for x in range(len(CMD_HELP)):
        table.add_row(list(CMD_HELP.keys())[x], list(CMD_HELP.values())[x])
    print(table)


def exit():
    clear()
    rule("[bold red]EXIT[/bold red]", style="bold red")
    quit()


def clear():
    os.system("cls || clear")


CMD_HELP = {
    "new": "Store a new password. Asks for a title (e.g. name of a site or service), password and optional notes.",
    "list": "Lists stored passwords. Doesnt display the actual password. (see '[bold]view[/bold]') ",
    "view [magenta]id/title[/magenta]": "View a password in plaintext using its id or title. (e.g. view 3 or view )",
    "rndpwd [magenta]N[/magenta]": "Generate a random password of length N",
    "help": "Displays this help message.",
    "exit [italic white]or[/italic white] quit": "Quit Keyholder."
}

CMD_LIST = {
    "new": new_password,
    "list": list_passwords,
    "view": view,
    "help": showhelp,
    "rndpwd": random_password,
    "exit": exit,
    "quit": exit,
}
