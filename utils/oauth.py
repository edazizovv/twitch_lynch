#
import json
import urllib.request


#
# https://dev.twitch.tv/docs/authentication#sending-user-access-and-app-access-tokens
# https://dev.twitch.tv/docs/authentication#getting-tokens
# https://dev.twitch.tv/docs/authentication
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#oauth-implicit-code-flow
# https://dev.twitch.tv/docs/authentication/getting-tokens-oauth

#
def get_token(client_id, client_secret):

    # url = 'https://id.twitch.tv/oauth2/authorize'

    scope = 'analytics:read:extensions+' \
            'analytics:read:games+' \
            'bits:read+' \
            'channel:read:hype_train+' \
            'channel:read:stream_key+' \
            'channel:read:subscriptions'

    # scope = ''

    # """
    url = 'https://id.twitch.tv/oauth2/token' \
          '?client_id={0}' \
          '&client_secret={1}' \
          '&grant_type={2}' \
          '&scope={3}'.format(client_id, client_secret, 'client_credentials', scope)

    # print(url)

    request = urllib.request.Request(url, method='POST')
    """

    url = 'https://id.twitch.tv/oauth2/authorize' \
          '?client_id={0}' \
          '&redirect_uri={1}' \
          '&response_type={2}' \
          '&scope={3}'.format(client_id, 'http://localhost', 'token', scope)

    print(url)

    request = urllib.request.Request(url, method='GET')

    """

    response = urllib.request.urlopen(request)

    result = json.loads(response.read())

    return result
