import time
from dataproc import *
from password_mgt import *
from console import print, rule
from commands import first_boot, CMD_LIST, login, command_processor, clear

master = ""

def main():
    # normal program loop here
    cmd = input("> ").lower().lstrip().rstrip()
    if len(cmd) == 0:
        pass
    elif cmd.split()[0] in CMD_LIST:
        command_processor(cmd)
    else:
        print('Unknown command (type "help" for a list of commands)')


if __name__ == "__main__":
    clear()
    pwd_data = {}

    if not PWD_FILE.is_file() and not DATA_FILE.is_file():
        # if we are here, this is the first run of the program
        try:
            first_boot()
        except KeyboardInterrupt:
            print("[red]Quitting...[/red]")
            quit()

    # login
    try:
        logged_in = login()
    except KeyboardInterrupt:
        print("[red]Login cancelled by user.[/red]")
        quit()
    
    if not logged_in:
        print("[red]Login failed.[/red]")
        quit()
    
    # main
    try:
        clear()
        print("[green]Logged in successfully.[/green]")
        time.sleep(0.8)
        clear()
        rule("[bold violet]Keyholder[/bold violet]", style="violet")
        print("\nWelcome! Type 'help' for help\n")
        while True:
            main()
    except KeyboardInterrupt:
        clear()
        rule("[bold red]EXIT[/bold red]", style="bold red")
