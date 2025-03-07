# checker.py

# Error checking functions
# Custom Exceptions

# Stephanie Lee
# stephl25@uci.edu
# 79834162

from pathlib import Path


class ErrorMessage(Exception):
    '''
    Error for when the server returns an 'error' message type
    '''
    pass


class InvalidEntry(Exception):
    '''
    Error for when an entry has an invalid value: None (except bio), "", or " "
    '''
    pass

class InvalidRecipient(Exception):
    pass

class NotConnected(Exception):
    pass

class CancelledEvent(Exception):
    pass

class AlreadyExistsError(Exception):
    pass

class Mismatched(Exception):
    pass

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
    if entry is not None and type(entry) is str:
        if len(entry) != 0 and not entry.isspace():
            return True
        else:
            raise InvalidEntry
    else:
        raise InvalidEntry


def check_existence(path: Path):
    if not path.exists():
        raise FileNotFoundError


def check_suffix(file_suffix):
    suffix = '.dsu'
    if not file_suffix == suffix:
        # File type exception
        raise TypeError

