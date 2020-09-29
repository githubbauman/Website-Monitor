#!/usr/bin/env python3

import os
import pathlib
import smtplib
import ssl

import config
from message import Message


class Mail:  # pylint: disable=too-few-public-methods

    @staticmethod
    def send(message_text):
        message = '''\
From: "''' + config.SENDER_NAME + '''" < ''' + config.SENDER_EMAIL + '''>
To: "''' + config.RECEIVER_NAME + '''" < ''' + config.RECEIVER_EMAIL + '''>
Subject: Website monitor

Dear ''' + config.RECEIVER_NAME + ''',

''' + message_text + '''
-- ''' + '''
Best regards,
''' + config.SENDER_NAME

        # Create a secure SSL context
        context = ssl.create_default_context()

        # Try to log in to server and send e-mail
        try:
            server = smtplib.SMTP(config.SMTP_SERVER, config.PORT)
            server.ehlo()
            server.starttls(context=context)  # Secure the connection
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.sendmail(
                config.SENDER_EMAIL,
                config.RECEIVER_EMAIL,
                message
            )
        except OSError as e:
            # Can't send e-mail. Write to log file.
            try:
                log_path = str(pathlib.Path(__file__).parent.absolute()) \
                       + os.path.sep \
                       + 'website_monitor.log'
                with open(log_path, 'a+') as filehandle:
                    log_text = Message.create('Mail not send. ' + str(e))
                    filehandle.write(message_text + log_text)
            # Can't send e-mail, can't write to file. Print to stout.
            except OSError as e:
                log_text = Message.create(
                    "Mail not send and can't write to log file"
                    + str(e)
                )
                print(message_text + log_text)
