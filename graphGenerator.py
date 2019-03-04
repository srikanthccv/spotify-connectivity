import requests, json, auth

def generateGraph():
    accessToken = auth.getAccessToken()
    print (accessToken)
    if accessToken is None:
        raise ValueError('Not a valid access token')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + accessToken
    }
    nodesList = ['A.R. Rahman']
    doneList = {}
    while len(nodesList) != 0:
        currentNode = nodesList.pop(0)
        print ('Current artist ' + currentNode)
        if currentNode not in doneList:
            doneList[currentNode] = True
            searchQueryParams = {
                'q': currentNode,
                'type': 'artist',
                'market': 'IN',
                'limit': 1
            }
            searchQueryResponse = requests.get('https://api.spotify.com/v1/search', headers=headers, params=searchQueryParams)
            if searchQueryResponse.status_code == 200:
                searchQueryResponse = json.loads(searchQueryResponse.text)
                artistSpotifyID = searchQueryResponse['artists']['items'][0]['id']
            else:
                print (searchQueryResponse.text)
                raise Exception('Invalid response')
            offset, limit, canProceed = 0, 50, True
            data = {
                'include_groups': 'single,album',
                'market': 'IN',
                'offset': offset,
                'limit': limit
            }
            while canProceed:
                resp = requests.get('https://api.spotify.com/v1/artists/{}/albums'.format(artistSpotifyID), headers=headers, params=data)
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
                            for artist in artistsList:
                                if artist not in doneList:
                                    nodesList.append(artist)
                else:
                    canProceed = False
                    print (resp.text) # error message

if __name__ == '__main__':
    generateGraph()
