import requests, json, auth

def go():
    access_token = auth.getAccessToken()
    print (access_token)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + access_token
    }
    offset, limit = 0, 50
    data = {
        'include_groups': 'single',
        'market': 'IN',
        'offset': offset,
        'limit': limit
    }
    resp = requests.get('https://api.spotify.com/v1/artists/1PDFenKwhb7oNx0bxCyQF2/albums', headers=headers, params=data)
    if resp.status_code == 200:
        resp = json.loads(resp.text)
        albums = resp['items']
        for album in albums:
            if len(album['artists']) != 1:
                print (album['name'])
                artistsList = [artist['name'] for artist in album['artists']]
                print (artistsList)

go()