import requests, json, auth

def go():
    access_token = auth.getAccessToken()
    print (access_token)
    if access_token is None:
        raise ValueError('Not a valid access token')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + access_token
    }
    offset, limit, canProceed = 0, 50, True
    data = {
        'include_groups': 'single,album',
        'market': 'IN',
        'offset': offset,
        'limit': limit
    }
    while canProceed:
        resp = requests.get('https://api.spotify.com/v1/artists/1mYsTxnqsietFxj1OgoGbG/albums', headers=headers, params=data)
        data['offset'] = data['offset'] + 50
        if resp.status_code == 200:
            resp = json.loads(resp.text)
            canProceed = (resp['next'] != None)
            albums = resp['items']
            for album in albums:
                if len(album['artists']) != 1:
                    print (album['name'])
                    artistsList = [artist['name'] for artist in album['artists']]
                    print (artistsList)
        else:
            canProceed = False
            print (resp.text) # error message

go()