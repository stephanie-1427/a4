'''
ds_messenger.py

Handles the client side of the program

Stephanie Lee
stephl25@uci.edu

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

    def set_recipient(self, new_recipient: str) -> None:
        '''
        Set the recipient to param new_recipient.

        :param new_recipient: Updated recipient.
        '''
        self.recipient = new_recipient

    def set_message(self, new_message: str) -> None:
        '''
        Set the message to param new_message.

        :param new_message: Updated message.
        '''
        self.message = new_message

    def set_timestamp(self, new_timestamp: float) -> None:
        '''
        Set the timestampe to param new_timestamp.

        :param new_timestamp: Updated timestamp.
        '''
        self.timestamp = new_timestamp

    def create_timestamp(self) -> None:
        '''
        Create a new timestamp and set it as the
        current timestamp.
        '''
        marked_time = time.time()
        self.set_timestamp(marked_time)


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
        connection_established = self.init_socket()
        if connection_established:
            return self.join()
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
            dm.set_recipient(recipient)
            dm.set_message(message)
            dm.create_timestamp()
            dsp.write(self.dsp_conn, dsp.format_directmsg(self.token, dm))
            return self.get_response()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return False

    def retrieve_new(self) -> list:
        '''
        Sends a formated retrieve new message to the server and returns the
        list of new messages sent to the user.
        '''
        try:
            dsp.write(self.dsp_conn, dsp.format_new(self.token))
            return self.get_inbox()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return None

    def retrieve_all(self) -> list:
        '''
        Sends a formated retrieve all message to the server and returns the
        list of all messages sent to the user.
        '''
        try:
            dsp.write(self.dsp_conn, dsp.format_all(self.token))
            return self.get_inbox()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return None

    def join(self):
        '''
        Joins a user to the server. Returns the join message
        received by the server if successful. None otherwise.
        '''
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
                server_msg = dsp.get_server_message(server_data)
                return server_msg
        except c.InvalidEntry:
            print('ERROR: Missing parameter(s).')
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
        except dsp.DSProtocolError as dsp_error:
            print(f"ERROR: {dsp_error}")

    def init_socket(self):
        '''
        Initilizes the socket and the protocol connection.
        '''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, 3001))
            self.dsp_conn = dsp.init(sock)
        except TypeError:
            print('ERROR: Parameter(s) of unexpected types.')
        except ConnectionRefusedError:
            # Only raised when no server is being run
            print('ERROR: Connection refused.')
        except socket.gaierror as s:
            print(f'ERROR: Address-related error: {s}')
        else:
            return True
        return False

    def get_response(self):
        '''
        Returns True if the message is accepted by server
        and server message is type "ok". False otherwise.
        '''
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            self.close_socket()
            return True
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return False

    def get_inbox(self):
        '''
        Returns the list of messages received by the server
        if message recieved from server is of type "ok".
        Returns None if the server message type is "error".
        '''
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            self.close_socket()
            inbox = dsp.get_server_messages(server_data)
            return inbox
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return None

    def close_socket(self):
        '''
        Call to close the socket.
        '''
        self.dsp_conn.socket.close()
