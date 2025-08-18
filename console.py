from rich import console

k_console = console.Console(highlight=False)

# overriding builtin print function with rich print
print = k_console.print
rule = k_console.rule
