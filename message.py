#!/usr/bin/env python3

from inspect import getframeinfo, stack
import datetime

from tzlocal import get_localzone


class Message:
    @staticmethod
    def create(message_text='Unknown message '):
    """Create message with date, time zone and line number.

    Args:
        message_text (str): Raw message.

    Returns:
        str: Message with date, time, time zone, file (caller)
             and line number (caller).
    """
        caller = getframeinfo(stack()[1][0])
        return("%s (%s) %s File: %s Line: %s\n" % (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            get_localzone(),
            message_text,
            caller.filename,
            caller.lineno,
        ))
