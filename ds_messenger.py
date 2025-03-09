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
        if self._init_socket():
            return self._join()

    def send(self, message: str, recipient: str) -> bool:
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
        try:
            dsp.write(self.dsp_conn, dsp.format_new(self.token))
            return self._get_inbox()
        except dsp.DSProtocolError as dsp_error:
            print(f'ERROR: {dsp_error}')
            return None

    def retrieve_all(self) -> list:
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
        return False

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
