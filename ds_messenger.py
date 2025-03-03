import ds_protocol as dsp
import checker as c
import socket
import time


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsp_conn = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
    
    def start_session(self):
        self._init_socket()
        self._join()

    def send(self, message:str, recipient:str) -> bool:
        dm = DirectMessage()
        dm.recipient = recipient
        dm.message = message
        dm.timestamp = time.time()
        dsp.write(self.dsp_conn, dsp.format_directmsg(self.token, dm))
        self._get_response()
        self._close_socket()
		
    def retrieve_new(self) -> list:
        dsp.write(self.dsp_conn, dsp.format_new(self.token))
        self._get_inbox()
        self._close_socket()
 
    def retrieve_all(self) -> list:
        dsp.write(self.dsp_conn, dsp.format_all(self.token))
        self._get_inbox()
        self._close_socket()
    
    def _join(self):
        '''
        Send user data to the server. Receive data from the server, print a reponse.
        Return a server generated token to be used for command calls.
        '''
        try:
            if self.token is None:
                self.token = ""
    
            if c.check_valid_entry(self.username) and c.check_valid_entry(self.password):
                dsp.write(self.dsp_conn, dsp.format_join(user=self.username, password=self.password, token=self.token))
                server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
                c.check_msg_type(dsp.get_msg_type(server_data))
                active_token = dsp.get_token(server_data)
                print_response(dsp.get_server_message(server_data))
                self.token = active_token
        except c.InvalidEntry:
            print('ERROR: Missing parameter(s).')
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
        except Exception as e:
            print(f"Uncaught Exception: {e}")
        else:
            return True
        return False

    def _init_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.dsuserver, 3001))
            self.dsp_conn = dsp.init(sock)
        except ValueError:
            print('ERROR: Invalid port.')
        except TypeError:
            print('ERROR: Parameter(s) of unexpected types.')
        except dsp.DSProtocolError:
            print('ERROR: Protocol issue')
        except ConnectionRefusedError:
            print('ERROR: Connection refused.')
        except socket.gaierror as s:
            print(f'ERROR: Address-related error: {s}')
        except Exception as e:
            print(f'ERROR: Undefined error {e}')
        else:
            return True
        return False

    def _get_response(self):
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            return True
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return False

    def _get_inbox(self):
        try:
            server_data = dsp.read_data(dsp.read_msg(self.dsp_conn))
            c.check_msg_type(dsp.get_msg_type(server_data))
            return dsp.get_server_messages(server_data)
        except c.ErrorMessage:
            print(f'ERROR: {dsp.get_server_message(server_data)}')
            return None
    
    def _close_socket(self):
        self.dsp_conn.socket.close()








# Use later
def print_inbox(server_messages: list):
    '''
    '''
    for msg in server_messages:
        print(f'Message: {msg["message"]}')
        print(f'From: {msg["from"]}')
        print(f'Sent: {msg["timestamp"]}')


def print_response(server_message: str, client_msg: str = None) -> None:
    '''
    Print a response using data received from the server

    :param server_message: The string message received from the server.
    :param client_msg: The string message (post or bio) from the client.
    :param current_token: The string value of the active token for the session.
    '''
    print(f'{server_message}')
    if client_msg is not None:
        print(f'---\n{client_msg}\n---')

