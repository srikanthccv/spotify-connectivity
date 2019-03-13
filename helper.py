import requests
import json
import authentication
from time import sleep


def wikiCheck(artist):
    wiki = 'https://en.wikipedia.org/w/api.php?action=opensearch&search={}&limit=1&format=json'.format(
        artist)
    wikiResponse = requests.get(wiki)
    if wikiResponse.status_code == 200:
        wikiResponse = wikiResponse.json()
        if len(wikiResponse) == 4 and wikiResponse[3]:
            wikiPage = requests.get(wikiResponse[3][0])
            if wikiPage.status_code == 200:
                if 'India' in wikiPage.text:
                    return True
    return False


def extractData():
    accessToken = authentication.getAccessToken()
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
            if requestsCnt % 100 == 0:
                sleep(30)
            searchQueryResponse = requests.get(
                'https://api.spotify.com/v1/search', headers=headers, params=searchQueryParams)
            requestsCnt = requestsCnt + 1
            if searchQueryResponse.status_code == 200:
                searchQueryResponse = searchQueryResponse.json()
                if (len(searchQueryResponse['artists']['items']) != 0):
                    if 'id' in searchQueryResponse['artists']['items'][0]:
                        artistSpotifyID = searchQueryResponse['artists']['items'][0]['id']
            else:
                continue
            offset, limit, canProceed = 0, 50, True
            data = {
                'include_groups': 'single,album',
                'market': 'IN',
                'offset': offset,
                'limit': limit
            }
            while canProceed:
                if requestsCnt % 100 == 0:
                    sleep(30)
                resp = requests.get('https://api.spotify.com/v1/artists/{}/albums'.format(
                    artistSpotifyID), headers=headers, params=data)
                requestsCnt = requestsCnt + 1
                data['offset'] = data['offset'] + 50
                if resp.status_code == 200:
                    resp = resp.json()
                    canProceed = (resp['next'] != None)
                    albums = resp['items']
                    for album in albums:
                        if len(album['artists']) != 1:
                            if album['name'] not in processedAlbumsList:
                                processedAlbumsList[album['name']] = True
                            else:
                                continue
                            collaboratorsList = [artist['name']
                                                 for artist in album['artists']]
                            indianCollaboratorsList = []
                            for artist in collaboratorsList:
                                if artist not in processedArtistsList and wikiCheck(artist):
                                    artistsList.append(artist)
                                    indianCollaboratorsList.append(artist)
                            if indianCollaboratorsList:
                                jsonBlob = {
                                    "album": album['name'],
                                    "artists": collaboratorsList,
                                    "album_url": album['external_urls']['spotify']
                                }
                                print(jsonBlob)
                else:
                    canProceed = False


if __name__ == '__main__':
    extractData()
