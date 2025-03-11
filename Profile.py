'''
Profile.py

Manages the profile object for storing data locally.

Original Author: Mark S. Baldwin, modified by Alberto Krone-Martins

Edited for ICS 32 a4 project use by:
Stephanie Lee
stephl25@uci.edu
79834162
'''
# No pylint catching for the file naming of Profile.py
# pylint: disable=invalid-name

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    '''
    Custom Exception for when the dsu file path or type is invalid
    '''


class DsuProfileError(Exception):
    '''
    Custom Exception for when the dsu file does not contain a
    profile object/json message.
    '''


class Message(dict):
    '''
    Creates a Message dict that stores all messages for the user,
    both sent and received.
    '''
    def __init__(self, entry: str = None,
                 timestamp: float = 0,
                 from_user: str = None,
                 to_user: str = None):
        self._timestamp = timestamp
        self.set_entry(entry)
        self.set_to_user(to_user)
        self.set_from_user(from_user)

        dict.__init__(self, entry=self._entry,
                      timestamp=self._timestamp,
                      from_user=self._from_user,
                      to_user=self._to_user)

    def set_to_user(self, to_user):
        '''
        Set a dict key and value for the user the message was sent to.
        '''
        self._to_user = to_user
        dict.__setitem__(self, 'to_user', to_user)

    def get_to_user(self):
        '''
        Get the user the message was sent to.
        '''
        return self._to_user

    def set_entry(self, entry):
        '''
        Set a dict key and value for the message content.
        '''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        if self._timestamp == 0:
            self._timestamp = f'{time.time()}'

    def get_entry(self):
        '''
        Get the message content.
        '''
        return self._entry

    def set_time(self, time: float):
        '''
        Set a dict key and value for the timestamp of the message.
        '''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        '''
        Get the timestamp for the message.
        '''
        return self._timestamp

    def set_from_user(self, from_user):
        '''
        Set a dict key and value for the user who sent the message.
        '''
        self._from_user = from_user
        dict.__setitem__(self, 'from_user', from_user)

    def get_from_user(self):
        '''
        Get the user who sent the message.
        '''
        return self._from_user

    user = property(get_to_user, set_to_user)
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    '''
    Handles the local storage of data. Stores messages and contacts added
    and stored by the user. Stores user data, including the selected
    dsuserver, username, and password.
    '''
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.friends = []
        self.messages = []

    def make_friend(self, user: str) -> None:
        '''
        Adds a username to the list of friends in the Profile object.

        :param user: The username to add to the self.friends list.
        '''
        self.friends.append(user)

    def del_friend(self, user: str) -> bool:
        '''
        Deletes a contact ("friend") from the friend list in the
        Profile object using a username.

        :param user: The username to delete from the self.friends list.
        '''
        try:
            if user in self.friends:
                self.friends.remove(user)
            return True
        except ValueError:
            return False

    def add_msg(self, msg: Message) -> None:
        '''
        Adds a Message object to the message list stored in
        the Profile object
        
        :param msg: The Message object to be added to the list self.messages
        '''
        self.messages.append(msg)

    def del_msg(self, index: int) -> bool:
        '''
        Deletes the Message in the Profile object at the
        specified index

        :param index: The index of the message list to delete.
        '''
        try:
            del self.messages[index]
            return True
        except IndexError:
            return False

    def get_messages(self) -> list[Message]:
        '''
        Returns the list of Messages stored in the Profile object.
        '''
        return self.messages

    def save_profile(self, path: str) -> None:
        '''
        save_profile accepts an existing dsu file to save the
        current instance of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        '''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        '''
        load_profile will populate the current instance of Profile
        with data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError
        '''
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.friends = obj['friends']
                    for msg_obj in obj['messages']:
                        msg = Message(msg_obj['entry'],
                                    msg_obj['timestamp'],
                                    msg_obj['from_user'],
                                    msg_obj['to_user'])
                        self.messages.append(msg)
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
