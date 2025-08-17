from password_mgt import *
import time
from console import print, rule
from rich.table import Table
from password_mgt import get_password, get_title, VALID_CHARS
from dataproc import *
from rich import box, prompt
import random
import sys

# view - view a password
# new - create a new password


def command_processor(cmd: str):
    if len(cmd.split()) > 1:
        CMD_LIST[cmd.split()[0]](cmd.split()[1])
    else:
        CMD_LIST[cmd]()


def login(*args) -> bool:
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
        password += random.choice(VALID_CHARS)
    print(password)


def new_password(*args):
    try:
        title = get_title()
        pwd = get_password("Enter new password: ", confirm=True)
        notes = input("Notes (optional): ")

        master_pwd = get_password("Enter your master password: ")
        while not auth(master_pwd):
            print("Password is wrong! Try again.")
            master_pwd = get_password("Enter your master password: ")

        with open(DATA_FILE, "rb") as f:
            if len(load_data()) == 0 or len(decrypt_data(load_data(), MASTER)) == 0:
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
        print(f"[green]Successfully stored password '{title}'[/green]")
    except KeyboardInterrupt:
        print("Cancelled new password creation.")


def view(*args):
    if len(args) == 0:
        print("[yellow]An id is required.[/yellow]")
        return
    
    try:
        id = int(args[0])
    except:
        print("[yellow]Invalid id.[/yellow]")
        return
    
    if len(load_data()) == 0 or len(decrypt_data(load_data(), MASTER)) == 0:
        print(f"No passwords stored.")
        return

    stored_pwd_data = decrypt_data(load_data(), MASTER)

    if id not in list(stored_pwd_data.keys()):
        print(f"No password with id {id}.")
        return

    master_pwd = get_password("Enter your master password: ")
    while not auth(master_pwd):
        print("Password is wrong! Try again.")
        master_pwd = get_password("Enter your master password: \r")
    stored_pwd_data = decrypt_data(load_data(), master_pwd)
    # abandoned the ctrl+c to clear idea
    try:
        print("\nThe password will auto-clear after 10 seconds.")
        print("[bold green]" + stored_pwd_data[id][1] + "[/]", end="\r")
        time.sleep(10)
        print(" "*(len(stored_pwd_data[id][1]) + 1))
    except KeyboardInterrupt:
        clear()
        print("Cleared console.")


#wip
def remove_password(*args):
    if len(args) == 0:
        print("[yellow]An id is required.[/yellow]")
        return
    
    try:
        id = int(args[0])
    except:
        print("[yellow]Invalid id.[/yellow]")
        return
    
    stored_pwd_data = decrypt_data(load_data(), MASTER)
    if id not in list(stored_pwd_data.keys()):
        print(f"No password with id {id}.")
        return
    choice = prompt.Prompt.ask(f"Are you sure you want to delete the password [cyan]'{stored_pwd_data[id][0]}'[/cyan]? (Y/n)")
    if choice.lower() not in ["y", "n"]:
        print("[yellow]Invalid choice.[yellow]")
        return
    if choice.lower() == "n":
        return
    master_pwd = get_password("Enter your master password: ")
    while not auth(master_pwd):
        print("Password is wrong! Try again.")
        master_pwd = get_password("Enter your master password: ")
    print(f"[green]Successfully deleted password '[white]{stored_pwd_data.pop(id)[0]}[/white]'[/green]")
    write_data(encrypt_data(stored_pwd_data, master_pwd))


def list_passwords(*args):
    if len(load_data()) == 0 or len(decrypt_data(load_data(), MASTER)) == 0:
        print("[yellow]No passwords stored.[/yellow]")
        return
    pwd_data = decrypt_data(load_data(), MASTER)
    table = Table(title="Stored passwords", box=box.ROUNDED)
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
    print(
        "!! [bold red]If you forget the master password, there is NO way to retrieve your stored passwords.[/bold red] !!"
    )
    time.sleep(2)
    set_master_password()
    datafile = open(DATA_FILE, "w").close()


def showhelp(*args):
    print("\nHere are the available commands:")
    table = Table(box=box.ROUNDED, show_lines=True)
    table.add_column("command", style="green")
    table.add_column("description")
    for x in range(len(CMD_HELP)):
        table.add_row(list(CMD_HELP.keys())[x], list(CMD_HELP.values())[x])
    print(table)


def exit(*args):
    clear()
    rule("[bold red]EXIT[/bold red]", style="bold red")
    sys.exit()


def clear(*args):
    os.system("cls || clear")



CMD_HELP = {
    "list": "Lists stored passwords. Doesnt display the actual password. (see '[bold]view[/bold]') ",
    "new": "Store a new password. Asks for a title (e.g. name of a site or service), password and optional notes.",
    "remove [magenta]id[/magenta]": "Remove a stored password using its id.",
    "view [magenta]id/title[/magenta]": "View a password in plaintext using its id. (e.g. view 3)",
    "help": "Displays this help message.",
    "exit [italic white]or[/italic white] quit": "Quit Keyholder."
}

CMD_LIST = {
    "new": new_password,
    "list": list_passwords,
    "view": view,
    "help": showhelp,
    "rndpwd": random_password,
    "remove": remove_password,
    "exit": exit,
    "quit": exit,
}
