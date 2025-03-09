# Profile.py

# Original Author: Mark S. Baldwin, modified by Alberto Krone-Martins

# Editing for a4 project use by:
# Stephanie Lee
# stephl25@uci.edu
# 79834162


import json
import time
from pathlib import Path


class DsuFileError(Exception):
    pass


class DsuProfileError(Exception):
    pass


class Message(dict):
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
        self._to_user = to_user
        dict.__setitem__(self, 'to_user', to_user)

    def get_to_user(self):
        return self._to_user

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        if self._timestamp == 0:
            self._timestamp = f'{time.time()}'

    def get_entry(self):
        return self._entry

    def set_time(self, time: float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        return self._timestamp

    def set_from_user(self, from_user):
        self._from_user = from_user
        dict.__setitem__(self, 'from_user', from_user)

    def get_to_user(self):
        return self._from_user

    user = property(get_to_user, set_to_user)
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.friends = []
        self.messages = []

    def make_friend(self, user: str) -> None:
        self.friends.append(user)

    def del_friend(self, user: str) -> bool:
        try:
            if user in self.friends:
                self.friends.remove(user)
            return True
        except ValueError:
            return False

    def add_msg(self, msg: Message) -> None:
        self.messages.append(msg)

    def del_msg(self, index: int) -> bool:
        try:
            del self.messages[index]
            return True
        except IndexError:
            return False

    def get_messages(self) -> list[Message]:
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
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
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
                f = open(p, 'r')
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
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
