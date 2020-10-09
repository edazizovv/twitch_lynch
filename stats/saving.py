
import time
import json
import pandas
import urllib
import datetime

from utils.oauth import get_token


def stream_counter(url, client_id, client_secret, n_catches=100, freeze=1):

    request = urllib.request.Request(url, method='GET')
    request.add_header("client-id", client_id)
    res = get_token(client_id=client_id, client_secret=client_secret)
    request.add_header("Authorization", "Bearer " + res['access_token'])

    timestamps = []
    viewers = []
    for j in range(n_catches):
        response = urllib.request.urlopen(request)
        tmpJSON = json.loads(response.read())
        if len(tmpJSON['data']) == 0:
            cur_viewers = 0
        else:
            cur_viewers = tmpJSON['data'][0]['viewer_count']
        viewers.append(cur_viewers)
        timestamps.append(datetime.datetime.now())
        time.sleep(freeze)
    data = pandas.DataFrame(data={'timestamp': timestamps, 'n_viewers': viewers})
    return data


