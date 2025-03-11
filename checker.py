'''
checker.py

Error checking functions
Custom Exceptions

Stephanie Lee
stephl25@uci.edu
79834162
'''

from pathlib import Path
from Profile import Profile


class ErrorMessage(Exception):
    '''
    Custom Exception when the server returns a message
    with type 'error'.
    '''


class InvalidEntry(Exception):
    '''
    Custom Exception when the entry is invalid according
    to some conditions.
    '''


class InvalidRecipient(Exception):
    '''
    Custom Exception for when the selected contact to send
    a message to is invalid (same as current user).
    '''


class NotConnected(Exception):
    '''
    Custom Exception raised when a client is not connected
    to a server or a file is not loaded.
    '''


class CancelledEvent(Exception):
    '''
    Custom Exception that is raised when an event
    in the GUI is cancelled.
    '''


class AlreadyExistsError(Exception):
    '''
    Custom Exception for when a contact is added, but it
    already exists. Ensures no duplicate contacts are
    added.
    '''


class Mismatched(Exception):
    '''
    Custom Exception for when usernames and/or passwords
    fail to match between active profile and stored profile
    in local file.
    '''


def check_msg_type(msg: str) -> None:
    '''
    Check the message type received from the server.
    Raise a dsp.ErrorMessage if message type is 'error'

    :param msg: The server message type received (either 'ok' or 'error').
    '''
    if msg == 'error':
        raise ErrorMessage


def check_valid_entry(entry) -> bool:
    '''
    Check the entry has a valid value.
    Return True if entry is not "", " ", or None.
    Raise dsp.InvalidEntry exception otherwise.

    :param entry: A string or NoneType entry.
    '''
    if entry is not None and isinstance(entry, str):
        if len(entry) != 0 and not entry.isspace():
            return True
    raise InvalidEntry


def check_existence(path: str) -> None:
    '''
    Checks the existence of path.
    Raise FileNotFoundError if path does not exist.

    :param path: The string of the path to check.
    '''
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError


def check_suffix(path: str) -> None:
    '''
    Checks the suffix of the path. Must be of type '.dsu'
    Raise TypeError if path suffix does not match.

    :param path: The string of the path to check.
    '''
    p = Path(path)
    suffix = '.dsu'
    if p.suffix != suffix:
        # File type exception
        raise TypeError


def check_match(profile: Profile, username: str, password: str) -> None:
    '''
    Matches the profile of a file to the username and password loaded
    in the direct messenger app.
    If it does not match, then raise a Mismatched Exception.

    :param profile: The profile object stored in the file.
    :param username: The username of the current session user.
    :param password: The password of the current session user.
    '''
    if profile.username != username or profile.password != password:
        raise Mismatched('Failed to open file. File info must match the current profile.')


def check_cancel(new_variable) -> None:
    '''
    Checks if an event was cancelled by checking if a variable is empty.
    Raise CancelledEvent Exception if new_variable is empty.

    :param new_variable: Can be of any type. The variable to check.
    '''
    if not new_variable:
        raise CancelledEvent


def check_connection(is_connected: bool) -> None:
    '''
    Checks if the client is connected to a server.
    Return NotConnected if the client is not connected to a server.

    :param is_connected: True/False if client is connected to a server.
    '''
    if not is_connected:
        raise NotConnected
