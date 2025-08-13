from dataproc import *
from password_mgt import *
from console import print
from pathlib import Path
from commands import first_boot, CMD_LIST, showhelp

pwd_file = Path("./pwd.dat")
data_file = Path("./data.dat")


def main():

    # normal program loop here
    cmd = input("> ").lower().lstrip().rstrip()
    if cmd in CMD_LIST:
        CMD_LIST[cmd]()
    else:
        print('Unknown command (type "help" for a list of commands)')


def test(id):
    t = input("Title: ")
    p = getpass()
    c = input("Comments: ")
    # titles[id], hash[id], comments[id] = t, p, c


if __name__ == "__main__":
    os.system("cls || clear")
    pwd_data = {}

    if not pwd_file.is_file() and not data_file.is_file():
        # if we are here, this is the first run of the program
        first_boot()
    showhelp()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Quitting...")
