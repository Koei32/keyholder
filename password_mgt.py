from getpass import getpass
import os
import pickle
from hashlib import sha256
from string import printable
from console import print
from secrets import compare_digest

valid_chars = printable[:-6]


def get_title() -> str:
    title = input("Title: ")
    if len(title) == 0:
        print("Title cannot be empty!")
        return get_title()
    return title


def get_password(
    prompt: str, check_validity: bool = False, confirm: bool = False
) -> str:
    pwd = getpass(prompt)

    if check_validity:
        match check_password_validity(pwd):
            case 1:
                print("Please choose a password that is atleast 8 characters long.")
                return get_password(prompt, check_validity, confirm)
            case 2:
                print("Password cannot contain whitespaces or non-ascii characters.")
                return get_password(prompt, check_validity, confirm)
            case 0:
                pass

    if confirm:
        cf_pwd = getpass("Confirm password: ")
        if pwd != cf_pwd:
            print("[bold red] Passwords do not match! [/bold red]")
            return get_password(prompt, check_validity, confirm)
        else:
            return pwd
    else:
        return pwd


def set_master_password():
    """
    Performs the whole procedure of setting a new master password.
    """
    pwd = getpass("New master password: ")
    match check_password_validity(pwd):
        case 1:
            print("Please choose a password that is atleast 8 characters long.")
            set_master_password()
            return
        case 2:
            print("Password cannot contain whitespaces or non-ascii characters.")
            set_master_password()
            return
        case 0:
            pass

    cf_pwd = getpass("Confirm master password: ")

    if pwd != cf_pwd:
        print("[bold red] Passwords do not match! [/bold red]")
        set_master_password()

    sha = sha256()
    salt = os.urandom(16)
    sha.update(pwd.encode() + salt)
    final_hash = sha.hexdigest()
    pwd_data = [final_hash, salt]
    with open("pwd.dat", "wb") as f:
        pickle.dump(pwd_data, f)
    print("[bold green]Master key set![/bold green]")


def auth(pwd: str) -> bool:
    """
    Compares hash of `pwd` with stored master password hash.
    ### Returns:
    `True` if the password matches\n
    `False` if the password doesnt match\n
    """
    with open("pwd.dat", "rb") as f:
        pwd_data = pickle.load(f)
    sha = sha256()
    sha.update(pwd.encode() + pwd_data[1])
    pwd_hash = sha.hexdigest()
    return compare_digest(pwd_data[0], pwd_hash)


def check_password_validity(pwd: str) -> int:
    """
    Checks validity of password string `pwd`.

    ### Returns:
    `0` if password is valid\n
    `1` if password is less than 8 characters long\n
    `2` if password contains invalid characters\n
    """
    if len(pwd) < 8:
        return 1
    for chr in pwd:
        if chr not in valid_chars:
            return 2
    return 0
