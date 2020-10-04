#
# source: https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
#
import socket
import logging
from emoji import demojize


#


#
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'learndatasci'
token = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1'
channel = '#ninja'

sock = socket.socket()

sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])

while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        logging.info(demojize(resp))
