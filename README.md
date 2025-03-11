Author: Stephanie Lee##
Contributors: ICS32 staff
Last Updated: 2025

Table of Contents:
TITLE
PROJECT DESCRIPTION
HOW TO INSTALL
RUNNING THE PROGRAM
SIMULATE RUNNING MULTIPLE CLIENTS
HOW TO USE THE PROJECT
CREDITS

TITLE
Direct Messenger App

PROJECT DESCRIPTION
Multiple clients/users hosted on a server can send messages to each other.
Tech stack used is python with help from the tkinter, socket, pathlib, and tying libraries.
Some challenges faced in the development of this application were automatic updates
and exception handling. These challenges were solved with a recursive function and
the python debugging tool, respectively.

HOW TO INSTALL
Clone the project from the github repository at *insert link*.
Once the project is loaded in your selected IDE, ensure all the libraries used are
installed on your local device. After all required libraries are installed, run the
server.py file in a dedicated terminal. Then, run the a4.py file in a dedicated terminal.
A tkinter window will automatically pop up and load.

RUNNING THE PROGRAM
The instructions displayed on the tkinter window will direct you how to use the application.
Go to settings and select "Configure DS Server" to join a server. Once a server is joined,
continue following the instructions prompted by the program. Go to file to create or open
a file. Once a file is opened, go to settings and select "Add Contact" to add a new contact.
A widget will pop up. Enter the username of the contact you wish to add and click "Ok." If
a file has been loaded, the contact should appear on the side of the window. Use the text
editor at the bottom of the application window to send messages. When a contact is selected,
sent and received messages for that contact will appear on the upper text box of the
application window.

SIMULATE RUNNING MULTIPLE CLIENTS
To simulate running multiple clients, duplicate the a4.py file. Run the base a4.py file in
a dedicated terminal. Then, run the duplicated a4.py file in a dedicated terminal. Two tkinter
windows will appear. This simulates running multiple clients. Follow the instructions in
RUNNING THE PROGRAM and continue.

HOW TO USE THE PROJECT
Function documentation is provided in ds_protocol.py if you are unfamiliar with the use
of a client-side protocol to communicate with a server.
ds_messenger.py handles the client-side of the application. Use the ds_messenger
module to send data to the server.
server.py handles the server-side of the application.
Profile.py aids in the local storage of data.
a4.py handles the GUI of the application.
To start the program from scratch, delete the store folder created by server.py. Then,
follow the instructions in RUNNING THE PROGRAM.
test_ds_messenger.py and test_ds_protocol.py are testing modules that test the functionality
of ds_messenger.py and ds_protocol.py using pytest.
checker.py consists of error/exception handling and custom Exceptions. The module only raises
Exceptions, it should not return anything (except for check_valid_entry).

CREDITS
Author of server.py: ICS32 staff
Code for Profile.py and the GUI in a4.py was created by ICS32 staff and edited for use
by Stephanie Lee.
