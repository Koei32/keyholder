# list - lists stored passwords
# view - view a password
# new - create a new password
# edit -
# delete -

from password_mgt import *
import time
from rich import print
from getpass import getpass
from password_mgt import check_password_validity, get_password, get_title

def new_password():
    title = get_title()
    pwd = get_password("Enter new password: ")
    note = input("Notes (optional): ")

    



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
    quit()
