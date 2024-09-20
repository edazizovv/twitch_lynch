#
# source: https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#

import argparse
import inspect

import socket
from emoji import demojize

import pandas
from zz import parse_comm_piece

#


def make_cli(func):

    parser = argparse.ArgumentParser()
    sig = inspect.signature(func)
    empty = inspect._empty

    for param in sig.parameters.values():
        annot = param.annotation
        options = {}

        if annot is empty:
            ptype = str
        elif isinstance(annot, tuple):
            ptype, help_msg = annot
            if help_msg is not empty:
                options['help'] = help_msg
        else:
            ptype = annot
        options['type'] = ptype
        if param.default is empty:
            options['required'] = True
        else:
            options['default'] = param.default
            if annot is empty:
                options['type'] = type(options['default'])

        name = param.name.replace('_', '-')
        parser.add_argument(f'--{name}', **options)

    func(**vars(parser.parse_args()))


#

def chats(channel):

    client_id_source = 'C:/Users/MainUser/Desktop/twitch_oauth.txt'
    crs = open(client_id_source, "r")
    for columns in (raw.strip().split() for raw in crs):
        oauth = columns[0]

    server = 'irc.chat.twitch.tv'
    # server = 'irc.twitch.tv'
    port = 6667
    nickname = 'redjerdai'
    token = oauth
    # channel = '#ilmasseo'

    sock = socket.socket()

    sock.connect((server, port))

    sock.send(f"PASS {token}\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\n".encode('utf-8'))
    sock.send(f"JOIN {channel}\n".encode('utf-8'))

    while True:
        resp = sock.recv(2048).decode('utf-8')

        if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

        elif nickname in resp:
            print(resp)

        elif len(resp) > 0:

            # logging.info(demojize(resp))
            splet = demojize(resp).split('\r\n')
            for s in splet:
                if s != '':
                    ry = pandas.DataFrame(parse_comm_piece(s))
                    to = './ry.csv'
                    import os
                    print(os.path.abspath(to))

                    ry.to_csv(to, index=False, mode='a', header=False)

chats('#letshe')
