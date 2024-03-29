#!/usr/bin/env python3

import http.server
import socketserver
import time
import os

from blessings import Terminal

t = Terminal()


def quickshell():
    cwd = os.getcwd()
    username = os.getlogin()
    print("[" + t.green("+") + "][" + username + ":" + cwd + "]$")
    print("[" + t.green("+") + "]Enter 'Q' to quit")
    try:
        while True:
            command = input("\n<" + t.cyan("SERVER") + ">$ ")
            if not command in ('q', 'Q'):
                os.system(command)
            else:
                print("\n[" + t.red("!") + "]Exiting shell")
                time.sleep(1.5)
                break

    except KeyboardInterrupt:
        print("\n[" + t.red("!") + "]Critical. User Aborted")


def invokeshell():
    print("[" + t.green("+") + "]Invoke a shell to make changes in server directory?")
    invoke = input("[" + t.magenta("?") + "][Y]es/[N]o: ").lower()
    if invoke == 'y':
        quickshell()
    elif invoke == 'n':
        print("[" + t.green("+") + "]Done")
    else:
        print("\n[" + t.red("!") + "]Unhandled Option")

print("\n[" + t.green("+") + "]Bootleg HTTP Server\n")

default = input("[" + t.magenta("?") + "]Default config? [Y]es/[N]o: ").lower()
if default == 'y':

    PORT = 8000
    IP = "127.0.0.1"
    invokeshell()
    print("\n[" + t.green("+") + "]Default config loaded\n")

elif default == 'n':

    print("[" + t.green("+") + "]Specify values:\n")
    PORT = eval(input("Port #: "))
    IP = input("Host IP: ")
    invokeshell()

else:
    print("\n[" + t.red("!") + "]Unhandled Option")


print("[" + t.green("+") + "]Starting Server...\n")

Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.webapp': 'application/x-web-app-manifest+json',
});

try:
    httpd = socketserver.TCPServer((IP, PORT), Handler)
except Exception as e:
    print("\n[" + t.red("!") + "]Critical! An exception was raised with the following error message:")
    print(e)

print("[" + t.green("+") + "]Serving at:", IP, repr(PORT))

# Watching keyboard interrupt
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n[" + t.red("!") + "]User Aborted")
