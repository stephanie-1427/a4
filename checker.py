# checker.py

# Error checking functions

# Stephanie Lee
# stephl25@uci.edu
# 79834162

from pathlib import Path


class OptionTypeError(Exception):
    pass


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


def check_required_attributes(attribute: str):
    if attribute is None or len(attribute) == 0 or attribute.isspace():
        raise SyntaxError


def check_option(option, supported_options: set):
    if option not in supported_options:
        raise OptionTypeError


def check_whitespace(entry: str):
    if entry.isspace() or len(entry) == 0:
        raise SyntaxError


def check_empty_entries(entry: str, valid_options: set):
    if entry in valid_options:
        raise SyntaxError


def check_dict_edge_cases(valid_entries: dict, raw_entries: list):
    if (len(valid_entries) == 0 or
            ((len(valid_entries.keys()) + len(valid_entries.values()))
                < len(raw_entries))):
        if not raw_entries[-1].startswith("-"):
            raise TypeError
        else:
            raise SyntaxError


def check_length(command: str, command_line_input: list):
    if ((command == 'C' and len(command_line_input) != 4) or
            (command in ('O', 'D', 'R') and len(command_line_input) != 2)):
        raise IndexError


def check_int(x):
    try:
        int(x)
        return
    except ValueError:
        raise ValueError


def check_existence(path: Path):
    if not path.exists():
        raise FileNotFoundError


def check_suffix(file_suffix):
    suffix = '.dsu'
    if not file_suffix == suffix:
        # File type exception
        raise TypeError


def check_file_is_loaded(file):
    if file is None:
        raise FileNotFoundError


def check_index(index: int, list_length: int):
    if not (0 <= index < list_length):
        raise IndexError


def check_index_special(valid_index: bool):
    if not valid_index:
        raise IndexError
