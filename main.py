import urllib.parse

import requests

headers = {
    'Authorization': '***REMOVED***'
}

names = [
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***',
    '***REMOVED***'
]

name = '***REMOVED***'
urlencoded_name = urllib.parse.quote_plus(name)
req = requests.get(url=f'https://apiv10.stolpejakten.no/toplists?type=-1&kommune=0&page=0&search={urlencoded_name}',
                   headers=headers)

print('\nStolpejakten API V10 GET Request:', req.url)
if req.status_code == 200:
    body = req.json()
    if body['count'] == 1:
        user = body['results'][0]
        user_name = user['user_name']
        score = user['score']
        rank = user['rank']
        print(f'{rank} | {user_name}: {score}')
else:
    print(f'Something went wrong: {req.status_code}: {req.text}')
