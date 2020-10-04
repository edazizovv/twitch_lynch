
import json
import urllib
import requests

"""
nickname = 'learndatasci'
token = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1'

API_URL = 'https://api.twitch.tv/kraken/streams/44322889'
data = {'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': 'uo6dggojyb8d6soh92zknwmi5ej1q2',
        'NICK': nickname,
        'PASS': token}

response = requests.get(API_URL, params=data)
"""

url = "https://api.twitch.tv/kraken/channel/?scope=channel_read/"
channel_id = urllib.request.Request(url)

channel_id.add_header("Client-ID", 'uo6dggojyb8d6soh92zknwmi5ej1q2')

#defined w/o "oath:" at the beginning
channel_id.add_header("Authorization", "OAuth " + 'CHANNEL_OAUTH')

response = urllib.request.urlopen(channel_id)
tmpJSON = json.loads(response.read())
print(str(tmpJSON['_id']))
