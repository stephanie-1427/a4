'''
ds_messenger.py

Handles the client side of the program

Stephanie Lee
stephl25@uci.edu
79834162
'''
import socket
import time
import ds_protocol as dsp
import checker as c


class DirectMessage:
    '''
    A DirectMessage object is created to store data needed for
    sending data to the server for directmessage command.
    '''
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    '''
    The message sending functionality. An object of DirectMessenger created
    to establish a connection to the server and send messages to the server.
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsp_conn = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password

    def start_session(self):
        '''
        Initializes the socket connection (DSConnection) in ds_protocol.
        And joins the user to the server.

        Returns the server message if joining the user is successful.
        Returns False otherwise.
        '''
        connection_established = self._init_socket()
        if connection_established:
            return self._join()
        return connection_established

    def send(self, message: str, recipient: str) -> bool:
        '''
        Sends a message to the recipient by creating a DirectMessage instance,
        passing it to protocol to format the message, and calling dsp.write to
        send the message to the server. Returns True is the message is
        successfully sent. False otherwise.

        :param recipient: The username of the user to send the message to.
        :param message: The message to be sent to the recipient
        '''
        try:
            dm = DirectMessage()
            dm.recipient = recipient
            dm.message = message
            dm.timestamp = time.time()
            dsp.write(self.dsp_conn, dsp.format_directmsg(self.token, dm))
            return self._get_response()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return False

    def retrieve_new(self) -> list:
        '''
        Sends a formated retreive new message to the server and returns the
        list of new messages sent to the user.
        '''
        try:
            dsp.write(self.dsp_conn, dsp.format_new(self.token))
            return self._get_inbox()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return None

    def retrieve_all(self) -> list:
        '''
        Sends a formated retreive all message to the server and returns the
        list of all messages sent to the user.
        '''
        try:
            dsp.write(self.dsp_conn, dsp.format_all(self.token))
            return self._get_inbox()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return None

    def _join(self):
        try:
            if self.token is None:
                self.token = ""

            if c.check_valid_entry(self.username) and c.check_valid_entry(self.password):
                dsp.write(self.dsp_conn,
                          dsp.format_join(user=self.username,
                                          password=self.password,
                                          token=self.token))
                server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
                c.check_msg_type(dsp.get_msg_type(server_data))
                active_token = dsp.get_token(server_data)
                self.token = active_token
                return dsp.get_server_message(server_data)
        except c.InvalidEntry:
            print('ERROR: Missing parameter(s).')
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
        except dsp.DSProtocolError as dsp_error:
            print(f"ERROR: {dsp_error}")

    def _init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, 3001))
            self.dsp_conn = dsp.init(sock)
        except TypeError:
            print('ERROR: Parameter(s) of unexpected types.')
        except ConnectionRefusedError:
            print('ERROR: Connection refused.')
        except socket.gaierror as s:
            print(f'ERROR: Address-related error: {s}')
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
        else:
            return True
        return False

    def _get_response(self):
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            self._close_socket()
            return True
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return False

    def _get_inbox(self):
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            self._close_socket()
            inbox = dsp.get_server_messages(server_data)
            return inbox
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return None

    def _close_socket(self):
        self.dsp_conn.socket.close()
