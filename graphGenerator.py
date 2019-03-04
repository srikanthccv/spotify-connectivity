import requests, json, auth
from time import sleep

def generateGraph():
    accessToken = auth.getAccessToken()
    requestsCnt = 1
    if accessToken is None:
        raise ValueError('Not a valid access token')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + accessToken
    }
    artistsList = ['A.R. Rahman']
    processedArtistsList = processedAlbumsList = {}
    while len(artistsList) != 0:
        currentArtist = artistsList.pop(0)
        if currentArtist not in processedArtistsList:
            processedArtistsList[currentArtist] = True
            searchQueryParams = {
                'q': currentArtist,
                'type': 'artist',
                'market': 'IN',
                'limit': 1
            }
            if requestsCnt%100 == 0:
                sleep(30)
            searchQueryResponse = requests.get('https://api.spotify.com/v1/search', headers=headers, params=searchQueryParams)
            requestsCnt = requestsCnt + 1
            if searchQueryResponse.status_code == 200:
                searchQueryResponse = json.loads(searchQueryResponse.text)
                artistSpotifyID = searchQueryResponse['artists']['items'][0]['id']
            else:
                raise Exception('Invalid response')
            offset, limit, canProceed = 0, 50, True
            data = {
                'include_groups': 'single,album',
                'market': 'IN',
                'offset': offset,
                'limit': limit
            }
            while canProceed:
                if requestsCnt%100 == 0:
                    sleep(30)
                resp = requests.get('https://api.spotify.com/v1/artists/{}/albums'.format(artistSpotifyID), headers=headers, params=data)
                requestsCnt = requestsCnt + 1
                data['offset'] = data['offset'] + 50
                if resp.status_code == 200:
                    resp = json.loads(resp.text)
                    canProceed = (resp['next'] != None)
                    albums = resp['items']
                    for album in albums:
                        if len(album['artists']) != 1:
                            if album['name'] not in processedAlbumsList:
                                processedAlbumsList[album['name']] = True
                            else:
                                continue
                            collaboratorsList = [artist['name'] for artist in album['artists']]
                            for artist in collaboratorsList:
                                if artist not in processedArtistsList:
                                    artistsList.append(artist)
                            jsonBlob = {
                                "album": album['name'],
                                "artists": collaboratorsList,
                                "album_url": album['external_urls']['spotify']
                            }
                            print (jsonBlob)
                else:
                    canProceed = False
                    print (resp.text) # error message

if __name__ == '__main__':
    generateGraph()
