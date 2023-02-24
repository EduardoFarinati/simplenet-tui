#!/usr/bin/env python3
"""
This file describes the main script of the simplenet TUI.
The idea is an interface to interactively send and receive
messages from a simplenet node.

For example: this script can be used to manipule the Flexfact
simulator, sending the events it expects and receiving the 
events it notifies.

Author: Eduardo Farinati Leite
Date: 20/02/2023
"""

import curses
import socket
import threading

import messages
import replies


# Define the IP address and port of the server
NODE_ADDRESSES = [("0.0.0.0", 40000), ("0.0.0.0", 40001)]

# Define the IP address and port of this script
ADDRESS = NODE_ADDRESSES[1]


def send_command(command):
    """Send the command to the server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((SERVER_IP, SERVER_PORT))
        tcp_socket.sendall(command.encode())
        response = tcp_socket.recv(1024).decode()
        return response.strip()


def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    # Draw the list of commands
    stdscr.addstr("Select a command:\n")
    for i, cmd in enumerate(COMMANDS):
        stdscr.addstr(f"{i+1}. {cmd}\n")
    stdscr.refresh()

    # Get user input and send the command to the server
    while True:
        key = stdscr.getkey()
        if key == "q":
            break
        try:
            cmd_index = int(key) - 1
            if cmd_index >= 0 and cmd_index < len(COMMANDS):
                command = COMMANDS[cmd_index]
                response = send_command(command)
                stdscr.addstr(f"\nServer response: {response}\n")
                stdscr.refresh()
        except ValueError:
            pass


if __name__ == "__main__":
    # Run the TUI
    curses.wrapper(main)
