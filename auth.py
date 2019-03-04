import requests, json
clientId = 'dd976765d83e46bab09dc98ef16d80eb'
clientSecret = '39ce6898fde54c91987e998cf81b9512'

def getAccessToken():
    headers = {'Authorization': 'Basic ZGQ5NzY3NjVkODNlNDZiYWIwOWRjOThlZjE2ZDgwZWI6MzljZTY4OThmZGU1NGM5MTk4N2U5OThjZjgxYjk1MTI='}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    if response.status_code == 200:
        response = json.loads(response.text)
        return response['access_token']
    else:
        print (response.text)
        return None