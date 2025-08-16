# Keyholder

<img src="https://files.catbox.moe/3shfq7.png"/>

Keyholder is a fully local, terminal-based password storage and management tool written in Python.

Keyholder makes use of the [cryptography](https://github.com/pyca/cryptography/) package for encryption and uses [rich](https://github.com/Textualize/rich) to render beautiful tables and formatted text.

## Features
I wrote this tool mostly for my personal use so its not the most feature loaded, but it is something. It supports securely adding, removing and viewing your stored passwords. The passwords are encrypted and then stored. <br>
The tool uses a master password system to authenticate the user. **If you forget the master password, you lose _ALL_ your stored passwords.**

## Commands
Here are some basic commands to get you started (you can type `help` to get the full list of commands):

<details>
  <summary>new - Store a new password</summary>
  Running `new` asks you the title to give to the password, the password itself and optional notes.
</details>
<details>
  <summary>list - Show a list of stored passwords</summary>
  Shows a list of the passwords stored in a table. This does not actually show the password in plaintext.
</details>
<details>
  <summary>view - View a password in plaintext</summary>
  Running <code>view ID</code> displays the password with id <code>ID</code> in plaintext for a few seconds.
</details>

## Examples


