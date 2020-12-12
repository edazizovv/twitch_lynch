
import time
import json
import pandas
import urllib.error
import urllib.parse
import urllib.request
import datetime


def handle_bad_gateway(request):
    try:
        response = urllib.request.urlopen(request)
    except TimeoutError as e:
        print(e)
        time.sleep(1)
        response = handle_bad_gateway(request)
    except Exception as e:
        if isinstance(e, urllib.error.HTTPError):
            print(e.reason)
            print(request.get_full_url())
            time.sleep(1)
            response = handle_bad_gateway(request)
        elif isinstance(e, urllib.error.URLError):
            print(e.reason)
            print(request.get_full_url())
            time.sleep(1)
            response = handle_bad_gateway(request)
        elif isinstance(e, urllib.error.URLError):
            print(e.reason)
            print(request.get_full_url())
            time.sleep(1)
            response = handle_bad_gateway(request)
        else:
            raise e
    return response


def get_id(client_id, control_token, user_login):
    # user_login_quoted = urllib.parse.quote(user_login)
    user_login_quoted = urllib.parse.quote_plus(user_login)
    request = 'https://api.twitch.tv/helix/users?login={0}'.format(user_login_quoted)
    request = urllib.request.Request(request, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)
    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    wow = json.loads(response.read())
    user_id = wow['data'][0]['id']
    return user_id


# def get_subscriptions(client_id, control_token, user_login):
def get_subscriptions(client_id, control_token, user_id):
    # user_id = get_id(client_id, control_token, user_login)
    request = 'https://api.twitch.tv/helix/users/follows?from_id={0}'.format(user_id)
    request = urllib.request.Request(request, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)
    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    wow = json.loads(response.read())
    # subd = [x['to_name'] for x in wow['data']]
    subd = [x['to_id'] for x in wow['data']]
    return subd


def get_subscribers(client_id, control_token, user_id):
    request = 'https://api.twitch.tv/helix/users/follows?to_id={0}'.format(user_id)
    request = urllib.request.Request(request, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)
    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    wow = json.loads(response.read())
    # subs = [x['from_name'] for x in wow['data']]
    subs = [x['from_id'] for x in wow['data']]
    return subs


def get_tags(client_id, control_token, user_id):
    request = 'https://api.twitch.tv/helix/streams/tags?broadcaster_id={0}'.format(user_id)
    request = urllib.request.Request(request, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)
    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    wow = json.loads(response.read())
    tags_names = [x['localization_names'] for x in wow['data']]
    tags_descr = [x['localization_descriptions'] for x in wow['data']]
    return tags_names, tags_descr


def get_top_games(client_id, control_token):
    request = 'https://api.twitch.tv/helix/games/top'
    request = urllib.request.Request(request, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)
    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    wow = json.loads(response.read())
    top_games_names = [x['name'] for x in wow['data']]
    return top_games_names


def get_currenty(client_id, control_token, user_login):

    user_id = get_id(client_id, control_token, user_login)

    url = 'https://api.twitch.tv/helix/streams?user_login={0}'.format(user_login)

    request = urllib.request.Request(url, method='GET')
    request.add_header("User-Agent", 'Mozilla/5.0')
    request.add_header("client-id", client_id)
    request.add_header("Authorization", "Bearer " + control_token)

    # response = urllib.request.urlopen(request)
    response = handle_bad_gateway(request)
    tmpJSON = json.loads(response.read())
    if len(tmpJSON['data']) == 0:
        is_active = 0
        cur_viewers = 0
    else:
        is_active = 1
        cur_viewers = tmpJSON['data'][0]['viewer_count']

    tags = get_tags(client_id, control_token, user_id)

    return is_active, tags, cur_viewers


def get_all(client_id, control_token, streamer_login):

    streamer_id = get_id(client_id, control_token, streamer_login)

    is_active, tags, n_viewers = get_currenty(client_id, control_token, streamer_login)

    subs = get_subscribers(client_id, control_token, streamer_id)
    subs_subd = {s: get_subscriptions(client_id, control_token, s) for s in subs}

    top_games = get_top_games(client_id, control_token)

    now_wow = datetime.datetime.now()
    streamers_subs = pandas.DataFrame(data={'timestamp': [now_wow] * len(subs), 'from': subs, 'to': [streamer_login] * len(subs)})

    subs_subd__subd_resc = [[x[0]] * len(x[1]) for x in list(subs_subd.items())]
    subs_subd__subs = [y for x in subs_subd__subd_resc for y in x]
    subs_subd__subd = [y for x in list(subs_subd.items()) for y in x[1]]
    subs_subd__n = len(list(subs_subd__subs))
    subs_subs = pandas.DataFrame(data={'timestamp': [now_wow] * subs_subd__n, 'from': subs_subd__subs, 'to': subs_subd__subd})

    to_sub = pandas.concat((streamers_subs, subs_subs), axis=0, ignore_index=True)
    to_cur = pandas.DataFrame(data={'timestamp': [now_wow], 'is_active': [is_active], 'tags': [tags], 'n_viewers': [n_viewers]})
    to_top = pandas.DataFrame(data={'timestamp': [now_wow] * len(top_games), 'rank': list(range(len(top_games))), 'game_name': top_games})

    return to_cur, to_sub, to_top


def parse_comm_piece(b):
    commenter = b[:b.index('!')]
    try:
        streamer = b[b.index("PRIVMSG ") + len("PRIVMSG "):][:b[b.index("PRIVMSG ") + len("PRIVMSG "):].index(" ")]
    except Exception as e:
        print(b)
        raise e
    message = b[b.index("PRIVMSG {0} :".format(streamer))+len("PRIVMSG {0} :".format(streamer)):]
    timestamp = datetime.datetime.isoformat(datetime.datetime.now())
    return {'commenter': [commenter], 'streamer': [streamer], 'message': [message], 'timestamp': [timestamp]}
