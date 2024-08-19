#!/usr/bin/env python3

import os
import sys
import time
import platform
import netifaces
import tkinter as tk
from tkinter import messagebox, ttk
import requests

LARGE_FONT = ("Verdana", 12)
BUTTON_FONT = ("Verdana", 10)

default_shell = "bash"

available_shells = [
    "bash", "php", "python", "python3", "perl", 'java',
    'javascript', 'node', "netcat", 'awk', 'gawk',
    'telnet', 'golang', 'powershell', 'tclsh', "ruby",
    "xterm", "ncat", "socket"
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TRHACKNON GUI Tool")
        self.geometry("400x400")

        self.configure(bg="#282c34")  
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=BUTTON_FONT, foreground="red", background="#61afef")
        self.style.configure("TLabel", font=LARGE_FONT, foreground="purple", background="#282c34")
        self.style.configure("TEntry", foreground="red", background="#3c4042")

        self.shell_label = ttk.Label(self, text="Select Shell:", style="TLabel")
        self.shell_label.pack(pady=10)

        self.shell_var = tk.StringVar(self)
        self.shell_var.set(default_shell)

        self.shell_menu = ttk.OptionMenu(self, self.shell_var, *available_shells)
        self.shell_menu.pack(pady=5)

        self.ip_label = ttk.Label(self, text="Enter IP Address:", style="TLabel")
        self.ip_label.pack(pady=10)

        self.ip_entry = ttk.Entry(self)
        self.ip_entry.pack(pady=5)

        self.detect_ip_button = ttk.Button(self, text="Detect IP", command=self.detect_ip, style="TButton")
        self.detect_ip_button.pack(pady=5)

        self.port_label = ttk.Label(self, text="Enter Port:", style="TLabel")
        self.port_label.pack(pady=10)

        self.port_entry = ttk.Entry(self)
        self.port_entry.insert(0, "1234")
        self.port_entry.pack(pady=5)

        self.start_button = ttk.Button(self, text="Start Listener", command=self.start_listener, style="TButton")
        self.start_button.pack(pady=20)

        self.exit_button = ttk.Button(self, text="Exit", command=self.quit, style="TButton")
        self.exit_button.pack(pady=5)

    def detect_ip(self):
        ip_list = []
        public_ip = None

        try:
            public_ip = requests.get('https://api.ipify.org').text
            ip_list.append(f"Public: {public_ip}")
        except requests.RequestException:
            messagebox.showwarning("IP Detection", "Could not detect public IP. Using local IP.")

        for interface in netifaces.interfaces():
            try:
                ip = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                ip_list.append(f"{interface}: {ip}")
            except (KeyError, IndexError):
                continue

        if ip_list:
            if public_ip:  
                self.ip_entry.delete(0, tk.END)
                self.ip_entry.insert(0, public_ip)
            else:  
                local_ip = ip_list[1].split(": ")[1] if len(ip_list) > 1 else None
                self.ip_entry.delete(0, tk.END)
                self.ip_entry.insert(0, local_ip)

            messagebox.showinfo("IP Detection", "\n".join(ip_list))
        else:
            messagebox.showwarning("IP Detection", "No IP address detected.")

    def start_listener(self):
        shell_type = self.shell_var.get()
        ip_address = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()

        if not ip_address:
            messagebox.showerror("Error", "IP Address cannot be empty.")
            return

        if not port.isdigit():
            messagebox.showerror("Error", "Port must be a valid number.")
            return

        confirmation = messagebox.askyesno("Start Listener", f"Start listener with {shell_type} shell on {ip_address}:{port}?")
        if confirmation:
            self.listener(int(port))

    def listener(self, port):
        messagebox.showinfo("Listener", f"Starting listener on port {port}...")
        os.system(f"netcat -lvnp {port}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
