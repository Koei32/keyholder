from dataproc import *
from password_mgt import *
from console import print
from pathlib import Path
from commands import first_boot, CMD_LIST, showhelp


def main():

    # normal program loop here
    cmd = input("> ").lower().lstrip().rstrip()
    if cmd.split(" ")[0] in CMD_LIST:
        CMD_LIST[cmd.split(" ")[0]](cmd.split(" ")[1])
    else:
        print('Unknown command (type "help" for a list of commands)')


if __name__ == "__main__":
    os.system("cls || clear")
    pwd_data = {}

    if not PWD_FILE.is_file() and not DATA_FILE.is_file():
        # if we are here, this is the first run of the program
        first_boot()
    showhelp()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Quitting...")
