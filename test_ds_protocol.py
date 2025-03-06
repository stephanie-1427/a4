import pytest
import ds_protocol as dsp
import socket

# mirrors DirectMessage class of ds_messenger.py
class DirectMessage():
    def __init__(self):
        self.recipient = 'to send'
        self.message = 'Hello World!'
        self.timestamp = 'random time stamp'

# TEST Init Function
def test_init():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        assert isinstance(dsp_connection, dsp.DSConnection)
        assert dsp_connection.socket == sock
        assert dsp_connection.token == None
        assert dsp_connection.timestamp == None

# TEST DSProtocolError on init
def test_DSProtocolError_init():
    with pytest.raises(dsp.DSProtocolError) as exception_info:
        dsp.init('badsocket')
    assert str(exception_info.value) == 'Invalid socket connection'

# TEST Write Function
def test_write():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        send_to_server = dsp.write(dsp_connection, {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}})
        assert send_to_server == None

# TEST DSProtocolError on write
def test_DSProtocolError_write():
    rand_dict = {"random": "dict"}
    with pytest.raises(dsp.DSProtocolError) as exception_info:
        dsp.write('writebeforeinit', rand_dict)
    assert str(exception_info.value) == 'Connection to write to server refused.'

# TEST Response
def test_read_msg():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        send_to_server = dsp.write(dsp_connection, {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}})
        assert send_to_server == None

    from_server = dsp.read_msg(dsp_connection)
    assert type(from_server) == str
    # from_server value will vary because of token

# TEST Read Functions
def test_read_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        send_to_server = dsp.write(dsp_connection, {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}})
        assert send_to_server == None

        from_server = dsp.read_msg(dsp_connection)
        assert type(from_server) == str

        data_from_server = dsp.read_data(from_server)
        assert isinstance(data_from_server, dsp.DataTuple)
        assert data_from_server.type == 'ok'
        # data_from_server.response will vary because of token

# TEST json.JSONDecodeError
def test_JSONDecodeError():
    bad_json_msg = '{"type": "ok", "message": "Direct message sent" '
    assert dsp.extract_json(bad_json_msg) == None

# TEST Format Functions
def test_format_join():
    # Non-empty token
    assert dsp.format_join('user', 'pwd', '2wed45ede45654edf456') == {"join": {"username": 'user', "password": 'pwd', "token": '2wed45ede45654edf456'}}
    assert type(dsp.format_join('user', 'pwd', '2wed45ede45654edf456')) == dict

    # Empty token
    assert dsp.format_join('user', 'pwd', '') == {"join": {"username": 'user', "password": 'pwd', "token": ''}}
    assert type(dsp.format_join('user', 'pwd', '')) == dict

def test_format_all():
    assert dsp.format_all('2wed45ede45654edf456') == {"token": '2wed45ede45654edf456', "directmessage": "all"}
    assert type(dsp.format_all('2wed45ede45654edf456')) == dict

def test_format_new():
    assert dsp.format_new('2wed45ede45654edf456') == {"token": '2wed45ede45654edf456', "directmessage": "new"}
    assert type(dsp.format_new('2wed45ede45654edf456')) == dict

def test_format_directmsg():
    dm_obj = DirectMessage()
    assert dsp.format_directmsg('2wed45ede45654edf456', dm_obj) == {"token": '2wed45ede45654edf456', "directmessage": {"entry": 'Hello World!', "recipient": 'to send', "timestamp": 'random time stamp'}}
    assert type(dsp.format_directmsg('2wed45ede45654edf456', dm_obj)) == dict

# TEST Getter Functions
def test_getter_functions():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        send_to_server = dsp.write(dsp_connection, {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}})
        assert send_to_server == None

        from_server = dsp.read_msg(dsp_connection)
        assert type(from_server) == str

        data_from_server = dsp.read_data(from_server)
        assert isinstance(data_from_server, dsp.DataTuple)

        assert dsp.get_msg_type(data_from_server) == 'ok'
        # token will vary, test the type
        assert type(dsp.get_token(data_from_server)) == str
        server_message = dsp.get_server_message(data_from_server)
        assert type(server_message) == str
        assert server_message in ('Welcome back, temp_user!', 'Welcome to ICS32 Distributed Social, temp_user!')

def test_get_server_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        dsp.write(dsp_connection, {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}})
        data_from_server = dsp.read_data(dsp.read_msg(dsp_connection))
        active_token = dsp.get_token(data_from_server)

        dsp.write(dsp_connection, {"token": active_token, "directmessage": "new"})
        server_messages = dsp.get_server_messages(dsp.read_data(dsp.read_msg(dsp_connection)))

        assert type(server_messages) == list
        # no directmessage is being called towards temp_user
        assert len(server_messages) == 0
        assert server_messages == []

if __name__ == "__main__":
    test_format_join()
    test_format_all()
    test_format_new()
    test_format_directmsg()

    test_init()
    test_DSProtocolError_init()

    test_write()
    test_DSProtocolError_write()

    test_read_data()
    test_read_msg()

    test_getter_functions()
    test_get_server_messages()

    test_JSONDecodeError()
