
import urllib

from stats.saving import stream_counter


# client_id_source = 'C:/Users/azizove/Desktop/twitch_client_id.txt'
client_id_source = 'C:/Users/MainUser/Desktop/twitch_client_id.txt'
crs = open(client_id_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_id = columns[0]

# client_secret_source = 'C:/Users/azizove/Desktop/twitch_client_secret.txt'
client_secret_source = 'C:/Users/MainUser/Desktop/twitch_client_secret.txt'
crs = open(client_secret_source, "r")
for columns in (raw.strip().split() for raw in crs):
    client_secret = columns[0]


# user_id = ''
# user_login = 'nickmercs'
user_login = 'berritv'
# user_login = 'ah0ra'

url = 'https://api.twitch.tv/helix/streams?user_login={0}'.format(user_login)

data = stream_counter(url, client_id, client_secret, n_catches=22000, freeze=1)
