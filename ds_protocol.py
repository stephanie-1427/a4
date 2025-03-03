# ds_protocol.py

# Stephanie Lee
# stephl25@uci.edu
# 79834162

import json
from collections import namedtuple
import socket

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'response'])
DSConnection = namedtuple('DSConnection', ['socket', 'send', 'recv', 'token', 'timestamp'])


class DSProtocolError(Exception):
    '''
    Error for when the socket fails to connect
    '''
    pass



def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object

    :param json_msg: The json string message to extract data from.
    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        type = json_obj['response']['type']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(type, response)


def init(sock: socket) -> DSConnection:
    '''
    Set up communication between the client and server.
    Establish a file to send data to the server.
    Establish a file to receive data from the server.
    Raise DSProtocolError when the client fails to connect to a server.

    :param sock: Initialized socket.
    '''
    try:
        f_send = sock.makefile('w')
        f_recv = sock.makefile('r')
    except Exception:
        raise DSProtocolError("Invalid socket connection")
    return DSConnection(
            socket=sock,
            send=f_send,
            recv=f_recv,
            token=None,
            timestamp=None
            )


def write(ds_conn: DSConnection, send_to_server: dict):
    '''
    Send a json message to the server

    :param ds_conn: The current DSConnection namedtuple that connects client to the server.
    :param send_to_server: The json formatted message to be sent to the server.
    '''
    try:
        json_msg = json.dumps(send_to_server)
        ds_conn.send.write(json_msg + '\r\n')
        ds_conn.send.flush()
    except Exception:
        raise DSProtocolError


def response(ds_conn: DSConnection):
    '''
    Receive a json formatted message from the server and return it as a string

    :param ds_conn: The current DSConnection namedtuple that connects client to the server.
    '''
    command_to_client = ds_conn.recv.readline()[:-1]
    return command_to_client


def read_msg(ds_conn: DSConnection):
    '''
    Wrapper for response

    :param ds_conn: The current DSConnection namedtuple that connects client to the server.
    '''
    return response(ds_conn)


def read_data(server_msg: str):
    '''
    Wrapper for extract_json

    :param server_msg: The raw server message formatted as a json string.
    '''
    return extract_json(server_msg)


def format_directmsg(user_token: str, dm_object):
    '''
    '''
    msg_dict = {"token": user_token, "directmessage": {"entry": dm_object.message, "recipient": dm_object.recipient, "timestamp": dm_object.time}}
    return msg_dict


def format_new(user_token: str):
    '''
    '''
    new_dict = {"token": user_token, "directmessage": "new"}
    return new_dict


def format_all(user_token: str):
    '''
    '''
    all_dict = {"token": user_token, "directmessage": "all"}
    return all_dict


def format_join(user=None, password=None, token=None):
    '''
    Format a join message and return the message as join_dict

    :param user: The user name collected or used to call.
    :param password: The password associated with the user name.
    :param token: The current token. "" will be passed until further notice.
    '''
    join_dict = {"join": {"username": user, "password": password, "token": token}}
    return join_dict


def format_post(user_token: str = None, post: str = None, current_time: float = None):
    '''
    Format a post message, store and return the message as post_dict

    :param user_token: The current token associated with the session.
    :param post: The message to be sent to the server.
    :param current_time: The timestamp for when the message is created and sent.
    '''
    post_dict = {"token": user_token, "post": {"entry": post, "timestamp": current_time}}
    return post_dict


def format_bio(user_token: str = None, bio: str = None, current_time: float = None):
    '''
    Format a bio message, store and return the message as bio_dict

    :param user_token: The current token associated with the session.
    :param bio: The updated or new bio to be sent to the server.
    :param current_time: The timestamp for when the message is created and sent.
    '''
    bio_dict = {"token": user_token, "bio": {"entry": bio, "timestamp": current_time}}
    return bio_dict


def get_server_message(data: DataTuple):
    '''
    Return server message

    :param data: DataTuple of the server message "response" and "token".
    '''
    return data.response['message']


def get_server_messages(data: DataTuple):
    '''
    Return server messages

    :param data: DataTuple of the server message "response" and "token"
    '''
    return data.response['messages']


def get_token(data: DataTuple):
    '''
    Return the current client token

    :param data: DataTuple of the server message "response" and "token".
    '''
    return data.response['token']


def get_msg_type(data: DataTuple):
    '''
    Return the server message type ('ok' or 'error')

    :param data: DataTuple of the server message "response" and "token".
    '''
    return data.type
