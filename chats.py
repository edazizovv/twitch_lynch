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
import sys

"""
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
"""

#


def chats(channel, no_id):

    channel = '#{0}'.format(channel)

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
        try:
            print('{0}: ick'.format(no_id))
            resp = sock.recv(2048).decode('utf-8')
            print('{0}: tick'.format(no_id))

            ## if resp.startswith('PING'):
            sock.send("PONG\n".encode('utf-8'))

            # elif nickname in resp:
            if nickname in resp:
                print(resp)

            elif len(resp) > 0:

                # logging.info(demojize(resp))
                splet = demojize(resp).split('\r\n')
                for s in splet:
                    if s != '':
                        print(s)
                        ry = pandas.DataFrame(parse_comm_piece(s))
                        to = 'C:/Users/MainUser/Desktop/ry.csv'

                        ry.to_csv(to, index=False, mode='a', header=False)
            print('{0}: ended'.format(no_id))

        except Exception as e:
            ee = str(e)
            rep = pandas.DataFrame(data={'j': [no_id], 'err_str': [ee]})
            to = 'C:/Users/MainUser/Desktop/rep.csv'

            rep.to_csv(to, index=False, mode='a', header=False)
"""
if __name__ == '__main__':
    make_cli(chats)
"""

import threading


def main():
    channels = ['olyavoodoo', 'ah0ra', 'olyashaa', 'igromania', 'thewide001',
                'ybicanoooobov', 'dendi', 'stray228', 's1mple', 'dreadztv', 'alohadancetv']
    threads = []
    for j in range(len(channels)):
        channel = channels[j]
        th = threading.Thread(target=chats, args=(channel, j))
        th.start()
        threads.append(th)


if __name__ == '__main__':
    main()
