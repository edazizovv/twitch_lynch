#
import time


#
from zz import get_all
from utils.oauth import get_token

#


client_id_source = 'C:/Users/MainUser/Desktop/twitch_client_id.txt'
crs = open(client_id_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_id = columns[0]

client_secret_source = 'C:/Users/MainUser/Desktop/twitch_client_secret.txt'
crs = open(client_secret_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_secret = columns[0]

res = get_token(client_id=client_id, client_secret=client_secret)

token_elapses = time.time() + res['expires_in'] - 100


def control_token():
    global token_elapses
    global res
    if time.time() > token_elapses:
        res = get_token(client_id=client_id, client_secret=client_secret)
        token_elapses = time.time() + res['expires_in'] - 100
    return res['access_token']


freeze = 1
to = './viewers'

# conda activate E:/venv/twitch_lynch
# cd C:/Sygm/RAMP/IP-02/OSTRTA/twitch_lynch
# python chats.py --channel 'alohadancetv'

user_logins = ['olyavoodoo', 'ah0ra', 'olyashaa', 'igromania', 'thewide001',
               'ybicanoooobov', 'dendi', 'stray228', 's1mple', 'dreadztv', 'alohadancetv']


while True:

    for user_login in user_logins:
        to_cur, to_sub, to_top = get_all(client_id, control_token(), streamer_login=user_login)
        to_cur.to_csv(to + '_CUR.csv', index=False, mode='a', header=False)
        to_sub.to_csv(to + '_SUB.csv', index=False, mode='a', header=False)
        to_top.to_csv(to + '_TOP.csv', index=False, mode='a', header=False)
        print(user_login)

    time.sleep(freeze)
    print('freeezeee.......')


"""

import time
import json
import pandas
import urllib
import datetime

freeze = 1
to = './viewers.csv'

client_id_source = 'C:/Users/MainUser/Desktop/twitch_client_id.txt'
crs = open(client_id_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_id = columns[0]

# client_secret_source = 'C:/Users/azizove/Desktop/twitch_client_secret.txt'
client_secret_source = 'C:/Users/MainUser/Desktop/twitch_client_secret.txt'
crs = open(client_secret_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_secret = columns[0]


user_logins = ['olyavoodoo', 'ah0ra', 'olyashaa', 'igromania', 'thewide001',
               'ybicanoooobov', 'dendi', 'stray228', 's1mple', 'dreadztv', 'dreadztv']

res = get_token(client_id=client_id, client_secret=client_secret)
token_access = res['access_token']
token_elapses = time.time() + res['expires_in'] - 100

while True:

    for user_login in user_logins:

        url = 'https://api.twitch.tv/helix/streams?user_login={0}'.format(user_login)

        request = urllib.request.Request(url, method='GET')
        request.add_header("client-id", client_id)

        if time.time() > token_elapses:
            res = get_token(client_id=client_id, client_secret=client_secret)
            token_access = res['access_token']
            token_elapses = time.time() + res['expires_in'] - 100

        request.add_header("Authorization", "Bearer " + token_access)

        timestamps = []
        viewers = []

        response = urllib.request.urlopen(request)
        tmpJSON = json.loads(response.read())
        if len(tmpJSON['data']) == 0:
            cur_viewers = 0
        else:
            cur_viewers = tmpJSON['data'][0]['viewer_count']
        viewers.append(cur_viewers)

        timestamps.append(datetime.datetime.now())

        data = pandas.DataFrame(data={'streamer': user_login, 'timestamp': timestamps, 'n_viewers': viewers})
        data.to_csv(to, index=False, mode='a', header=False)
        print(user_login)

    time.sleep(freeze)
    print('freeezeee.......')
"""