# Stephanie Lee
# stephl25@uci.edu
# 79834162


import socket
import time
import ds_protocol as dsp


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((server, port))
      dsp_connection = dsp.init(sock)
      active_token = ""

      if check_valid_entry(username) and check_valid_entry(password):
        active_token = join(dsp_connection, username, password, active_token)

      if bio is None:
        if check_valid_entry(message):
          post_command(dsp_connection, active_token, message)
      elif bio is not None:
        if len(message) == 0 and check_valid_entry(bio):
          bio_command(dsp_connection, active_token, bio)
        elif check_valid_entry(message) and check_valid_entry(bio):
          post_command(dsp_connection, active_token, message)
          bio_command(dsp_connection, active_token, bio)

  except ValueError:
    print('ERROR: Invalid port.')
  except TypeError:
    print('ERROR: Parameter(s) of unexpected types.')
  except dsp.InvalidEntry:
    print('ERROR: Missing parameter(s).')
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


def join(dsp_conn: dsp.DSConnection, username: str, password: str, current_token: str) -> str:
  '''
  Send user data to the server. Receive data from the server, print a reponse.
  Return a server generated token to be used for following post and bio command calls.

  :param dsp_conn: The initialized DSConnection from the ds_protocol module.
  :param username: The user name entered in the send function call.
  :param password: The password entered in the send function call.
  :param current_token: An empty string ""
  '''
  try:
    dsp.write(dsp_conn, dsp.format_join(user=username, password=password, token=current_token))
    server_data = dsp.read_data(dsp.read_msg(dsp_conn))
    check_msg_type(dsp.get_msg_type(server_data))
    active_token = dsp.get_token(server_data)
    print_response(dsp.get_server_message(server_data))
    return active_token
  except dsp.ErrorMessage:
    print(f'ERROR: {dsp.get_server_message(server_data)}')


def post_command(dsp_conn: dsp.DSConnection, current_token: str, message: str) -> None:
  '''
  Send post data to the server. Receive data from the server and print a reponse.

  :param dsp_conn: The initialized DSConnection from the ds_protocol module.
  :param current_token: The active token that associates with the session.
  :param message: The post to be sent to the server.
  '''
  dsp.write(dsp_conn, dsp.format_post(user_token=current_token, post=message, current_time=time.time()))
  get_response(dsp_conn, message)


def bio_command(dsp_conn: dsp.DSConnection, current_token: str, user_bio: str) -> None:
  '''
  Send bio data to the server. Receive data from the server and print a reponse.

  :param dsp_conn: The initialized DSConnection from the ds_protocol module.
  :param current_token: The active token that associates with the session.
  :param user_bio: The new or updated bio to be sent to the server.
  '''
  dsp.write(dsp_conn, dsp.format_bio(user_token=current_token, bio=user_bio, current_time=time.time()))
  get_response(dsp_conn, user_bio)


def new_command(dsp_conn: dsp.DSConnection, current_token: str):
  '''
  '''
  dsp.write(dsp_conn, dsp.format_new(current_token))
  get_response(dsp_conn, directmessages=True)


def all_command(dsp_conn: dsp.DSConnection, current_token: str):
  '''
  '''
  dsp.write(dsp_conn, dsp.format_all(current_token))
  get_response(dsp_conn, directmessages=True)


def msg_command():
  '''
  '''
  pass


def get_response(dsp_conn: dsp.DSConnection, client_msg: str = None, directmessages: bool = False):
  '''
  Get data from the server using communication with protocol.
  Print a response according to the data retrieved.

  :param dsp_conn: The initialized DSConnection from the ds_protocol module.
  :param client_msg: The post or bio message sent to the server.
  '''
  try:
    server_data = dsp.read_data(dsp.read_msg(dsp_conn))
    check_msg_type(dsp.get_msg_type(server_data))
    if not directmessages:
      print_response(dsp.get_server_message(server_data), client_msg)
    else:
      print_response(dsp.get_server_messages(server_data))
  except dsp.ErrorMessage:
    print(f'ERROR: {dsp.get_server_message(server_data)}')


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


def check_msg_type(msg: str) -> None:
  '''
  Check the message type received from the server.
  Raise a dsp.ErrorMessage if message type is 'error'

  :param msg: The server message type received (either 'ok' or 'error').
  '''
  if msg == 'error':
    raise dsp.ErrorMessage


def check_valid_entry(entry) -> bool:
  '''
  Check the entry has a valid value.
  Return True if entry is not "", " ", or None.
  Raise dsp.InvalidEntry exception otherwise.

  :param entry: A string or NoneType entry.
  '''
  if entry is not None and type(entry) is str:
    if len(entry) != 0 and not entry.isspace():
      return True
    else:
      raise dsp.InvalidEntry
  else:
    raise dsp.InvalidEntry
