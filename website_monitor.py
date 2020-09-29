#!/usr/bin/env python3
import hashlib
import os
import pathlib
import pickle
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup

import config
from mail import Mail
from message import Message


def website_monitor():
    message_text = ''
    websites_hashes_path = \
        str(pathlib.Path(__file__).parent.absolute()) \
        + os.path.sep \
        + 'website_monitor.data'

    try:
        with open(websites_hashes_path, 'rb') as filehandle:
            # Pickle can read/write datastructures in a file
            websites_hashes = pickle.load(filehandle)
    except OSError as e:
        # Not a dictonary file created yet or not readable.
        # Create new empty dictionary.
        websites_hashes = {}
        message_text += Message.create(e)

    for website in config.WEBSITES:
        try:
            response = urlopen(website, timeout=3).read()
        except HTTPError as e:
            message_text += Message.create(
                website
                + ' HTTP error. '
                + str(e.reason)
            )
        except URLError as e:
            if isinstance(e.reason, socket.timeout):
                message_text += Message.create(
                    website
                    + ' URL error. '
                    + str(e.reason)
                )
            else:
                # See: https://stackoverflow.com/questions/8763451/
                message_text += Message.create(website + ' ' + str(e.reason))
        else:
            # Only checking body for changes.
            # Don't want to be triggered by websites
            # changing their header every request (e.g. nonce).
            soup = BeautifulSoup(response, 'html.parser')
            current_hash = hashlib.md5(soup.body.encode()).hexdigest()
            if website in websites_hashes:
                previous_hash = websites_hashes[website]
                if current_hash != previous_hash:
                    message_text += Message.create(
                        website + ' Website changed.'
                    )
                    websites_hashes[website] = current_hash
                # No errors, website works fine.
                elif config.EMAIL_WITHOUT_ERRORS:
                    message_text += Message.create(website + ' No errors.')
            else:
                # Website is not in dictionary. Add website (and hash) to
                # dictionary.
                websites_hashes[website] = current_hash
                message_text += Message.create(
                    website + ' No previous data known. New website added.'
                )
    # Write dictionary to file.
    try:
        with open(websites_hashes_path, 'wb') as filehandle:
            pickle.dump(websites_hashes, filehandle)
    except OSError as e:
        message_text += Message.create(str(e))

    if message_text:
        Mail.send(message_text)
        # Debug
        # print(message_text)


if __name__ == '__main__':
    website_monitor()
