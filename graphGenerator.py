import requests, json, auth

def generateGraph():
    access_token = auth.getAccessToken()
    print (access_token)
    if access_token is None:
        raise ValueError('Not a valid access token')
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer ' + access_token
    }
    nodesList = ['A.R. Rahman']
    doneList = {}
    while len(nodesList) != 0:
        currentNode = nodesList.pop(0)
        if doneList[currentNode] is None:
            doneList[currentNode] = True
            searchQueryParams = {
                'q': currentNode,
                'type': 'artist',
                'market': 'IN',
                'limit': 1
            }
            searchQueryResponse = requests.get('https://api.spotify.com/v1/search', headers=headers, params=searchQueryParams)
            if searchQueryResponse.status_code == 200:
                searchQueryResponse = json.loads(searchQueryResponse)
                artistSpotifyID = searchQueryResponse['id']
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
                else:
                    canProceed = False
                    print (resp.text) # error message

if __name__ == '__main__':
    generateGraph()
