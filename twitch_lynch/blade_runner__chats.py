
import urllib

from chats.saving import track_chat


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

my_nickname = 'bobbi_hatt'
# user_id = ''
# user_login = 'nickmercs'
# user_login = 'berritv'
# user_login = 'ah0ra'
user_login = 'stray228'

track_chat(server='irc.chat.twitch.tv', port=6667, nickname=my_nickname,
           client_id=client_id, client_secret=client_secret, target_channel=user_login, timelen=100)
