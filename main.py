import urllib.parse

import requests

headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJVc2VySWQiOiI2NjIxMTY0NmI5MTk4M2ViNTUxNDFiNWIiLCJVc2VyRGlzcGxheU5hbWUiOiJCcmVkZSBGcml0am9mIEtsYXVzZW4iLCJqdGkiOiI2MzE3NjY1MS0xMzQ1LTQzNjctYTdjYi0wM2ZlN2U3NjdiNjgiLCJyb2xlIjoidXNlciIsIm5iZiI6MTcxNDA2NDkyMywiZXhwIjoxNzE0MDkzNzIzLCJpYXQiOjE3MTQwNjQ5MjMsImlzcyI6InN0b2xwZWpha3RlbiIsImF1ZCI6InN0b2xwZWpha3RlbiJ9.E_mRUlIo6aqjPdUZNQ_FUI4pQEKXR4u4z9YCRPALfzO1IA-NSXLLRdfVR1JUtV9z3VfS_TFE4gX_7SzIFh8UlA'
}

names = [
    'Brede Fritjof Klausen',
    'frodo',
    'Malene Helsem',
    'Robin Svanor',
    'André',
    'Espen Øvestad',
    'Olav'
]

name = 'Brede Fritjof Klausen'
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
