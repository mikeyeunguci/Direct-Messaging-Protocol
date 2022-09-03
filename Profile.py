# Rio Suzuki
# rios@uci.edu
# 78627374

# Michael Yeung
# myeung2@uci.edu
# 71598323

# ICS 32 Fall 2021
# Assignment #2: Journal
#
# Author: Mark S. Baldwin
#
# v0.1.7

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#
# YOU DO NOT NEED TO READ OR UNDERSTAND THE JSON SERIALIZATION ASPECTS OF THIS CODE RIGHT NOW, 
# though can you certainly take a look at it if you are curious.
#
import json, time, os
from pathlib import Path
from ds_messenger import DirectMessage


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.
    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.
    """
    pass

class RecipientNotFound(Exception):
    """
    Raised when the recipient is not found.
    """
    pass


class Profile:
    """
    The Profile class exposes the properties required to join an ICS 32 DSU server. You will need to 
    use this class to manage the information provided by each new user created within your program for a2. 
    Pay close attention to the properties and functions in this class as you will need to make use of 
    each of them in your program.

    When creating your program you will need to collect user input for the properties exposed by this class. 
    A Profile class should ensure that a username and password are set, but contains no conventions to do so. 
    You should make sure that your code verifies that required properties are set.
    """

    def __init__(self, dsuserver=None, username="", password=""):
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.bio = ''
        self.chats = {}

    def add_dm(self, recipient:str, dm:DirectMessage):
        """
        Adds the dm to the dsu file
        """
        try:
            self.chats[recipient].append(dm)
        except Exception as e:
            raise RecipientNotFound(e)

    def save_profile(self, path: str) -> None:
        """
        save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError
        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                test = json.dumps(self.__dict__)
                f.write(test)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """

        load_profile will populate the current instance of Profile with data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                #for dm_obj in obj['dms']:
                #    dm = DirectMessage(dm_obj["from"], dm_obj["message"], dm_obj["timestamp"])
                #    self.dms.append(dm)
                self.chats = obj['chats']
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
