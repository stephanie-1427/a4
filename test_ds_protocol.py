'''
test_ds_protocol.py

Tests the functionality of ds_protocol.py

Stephanie Lee
stephl25@uci.edu
79834162
'''
import socket
import pytest
import ds_protocol as dsp

class DirectMessage():
    '''
    Mirrors DirectMessage class of ds_messenger.py
    '''
    def __init__(self):
        self.recipient = 'to send'
        self.message = 'Hello World!'
        self.timestamp = 'random time stamp'


def test_init():
    '''
    Tests the init() function of ds_protocol.py
    Asserts the DSConnection namedtuple is established correctly.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        assert isinstance(dsp_connection, dsp.DSConnection)
        assert dsp_connection.socket == sock
        assert dsp_connection.token is None
        assert dsp_connection.timestamp is None


def test_ds_protocol_error_init():
    '''
    Tests that DSProtocolError is being raised and handled
    properly when raised in init()
    '''
    with pytest.raises(dsp.DSProtocolError) as exception_info:
        dsp.init('badsocket')
    assert str(exception_info.value) == 'Invalid socket connection'


def test_write():
    '''
    Tests the write functionality of ds_protocol.py
    Simulates joining a user to the server.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        join_msg = {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}}
        assert dsp.write(dsp_connection, join_msg) is None


def test_ds_protocol_error_write():
    '''
    Tests that DSProtocolError is being raised and handled
    properly when raised in write()
    '''
    rand_dict = {"random": "dict"}
    with pytest.raises(dsp.DSProtocolError) as exception_info:
        dsp.write('writebeforeinit', rand_dict)
    assert str(exception_info.value) == 'Connection to write to server refused.'


def test_read_msg():
    '''
    Tests the wrapper method read_msg() for response() in ds_protocol.py.
    Indirectly tests the response() method.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        join_msg = {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}}
        assert dsp.write(dsp_connection, join_msg) is None

    from_server = dsp.read_msg(dsp_connection)
    assert isinstance(from_server, str)
    # from_server value will vary because of token


def test_read_data():
    '''
    Tests the wrapper method read_data() for extract_json() in ds_protocol.py.
    Indirectly tests the extract_json() method.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        join_msg = {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}}
        assert dsp.write(dsp_connection, join_msg) is None

        from_server = dsp.read_msg(dsp_connection)
        assert isinstance(from_server, str)

        data_from_server = dsp.read_data(from_server)
        assert isinstance(data_from_server, dsp.DataTuple)
        assert data_from_server.type == 'ok'
        # data_from_server.response will vary because of token


def test_json_decode_error():
    '''
    Tests the JSONDecodeError Exception in extract_json() is raised
    and handled properly.
    '''
    bad_json_msg = '{"type": "ok", "message": "Direct message sent" '
    assert dsp.extract_json(bad_json_msg) is None


def test_getter_functions():
    '''
    Tests all get_ functions in ds_protocol.py except for
    get_server_messages. Testing grouped together to reduce
    repeated code.
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        join_msg = {"join": {"username": 'temp_user', "password": 'temp_password', "token": ''}}
        assert dsp.write(dsp_connection, join_msg) is None

        from_server = dsp.read_msg(dsp_connection)
        assert isinstance(from_server, str)

        data_from_server = dsp.read_data(from_server)
        assert isinstance(data_from_server, dsp.DataTuple)

        assert dsp.get_msg_type(data_from_server) == 'ok'
        # token will vary, test the type
        assert isinstance(dsp.get_token(data_from_server), str)
        server_message = dsp.get_server_message(data_from_server)
        assert isinstance(server_message, str)
        assert server_message in ('Welcome back, temp_user!',
                                  'Welcome to ICS32 Distributed Social, temp_user!')


def test_get_server_messages():
    '''
    Tests get_server_messages() function in ds_protocol.py
    '''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('127.0.0.1', 3001))
        dsp_connection = dsp.init(sock)
        dsp.write(dsp_connection, {"join": {"username": 'temp_user',
                                            "password": 'temp_password',
                                            "token": ''}})
        data_from_server = dsp.read_data(dsp.read_msg(dsp_connection))
        active_token = dsp.get_token(data_from_server)

        dsp.write(dsp_connection, {"token": active_token, "directmessage": "new"})
        server_messages = dsp.get_server_messages(dsp.read_data(dsp.read_msg(dsp_connection)))

        assert isinstance(server_messages, list)
        # no directmessage is being called towards temp_user
        assert len(server_messages) == 0
        assert server_messages == []


def test_format_join():
    '''
    Tests the format_join() method in ds_protocol.py makes a
    correctly formatted dict and has type dict.
    '''
    # Non-empty token
    token_dict = dsp.format_join('user', 'pwd', '2wed45ede45654edf456')
    assert token_dict == {"join": {"username": 'user',
                                   "password": 'pwd',
                                   "token": '2wed45ede45654edf456'}}
    assert isinstance(token_dict, dict)

    # Empty token
    empty_token_dict = dsp.format_join('user', 'pwd', '')
    assert empty_token_dict == {"join": {"username": 'user', "password": 'pwd', "token": ''}}
    assert isinstance(empty_token_dict, dict)


def test_format_all():
    '''
    Tests the format_all() method in ds_protocol.py makes a
    correctly formatted dict and has type dict.
    '''
    returned_dict = dsp.format_all('2wed45ede45654edf456')
    assert returned_dict == {"token": '2wed45ede45654edf456', "directmessage": "all"}
    assert isinstance(returned_dict, dict)


def test_format_new():
    '''
    Tests the format_all() method in ds_protocol.py makes a
    correctly formatted dict and has type dict.
    '''
    returned_dict = dsp.format_new('2wed45ede45654edf456')
    assert returned_dict == {"token": '2wed45ede45654edf456', "directmessage": "new"}
    assert isinstance(returned_dict, dict)


def test_format_directmsg():
    '''
    Tests the format_directmsg() method in ds_protocol.py makes a
    correctly formatted dict and has type dict.
    '''
    dm_obj = DirectMessage()
    returned_dict = dsp.format_directmsg('2wed45ede45654edf456', dm_obj)
    assert returned_dict == {"token": '2wed45ede45654edf456',
                             "directmessage": {"entry": 'Hello World!',
                                               "recipient": 'to send',
                                               "timestamp": 'random time stamp'}}
    assert isinstance(returned_dict, dict)


if __name__ == "__main__":
    test_format_join()
    test_format_all()
    test_format_new()
    test_format_directmsg()

    test_init()
    test_ds_protocol_error_init()

    test_write()
    test_ds_protocol_error_write()

    test_read_data()
    test_read_msg()

    test_getter_functions()
    test_get_server_messages()

    test_json_decode_error()
