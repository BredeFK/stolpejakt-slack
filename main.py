import json
import os
import urllib.parse

import requests
from Member import Member
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

with open('members.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

member_names = [line.strip() for line in lines]
print(member_names)
members = []

for name in member_names:
    urlencoded_name = urllib.parse.quote_plus(name)
    req = requests.get(url=f'https://apiv10.stolpejakten.no/toplists?type=-1&kommune=0&page=0&search={urlencoded_name}',
                       headers={'Authorization': f'Bearer {TOKEN}'})

    if req.status_code == 200:
        body = req.json()
        if body['count'] == 1:
            user = body['results'][0]
            member = Member(user['rank'], user['user_name'], int(user['score']))
            members.append(member)
            # print(f'{member.rank} | {member.user_name}: {member.score}')
        else:
            members.append(Member('NOT FOUND', name, -1))
            print(f'Found more than one user with name {name}')
    else:
        print(f'Something went wrong: {req.status_code}: {req.text}')

sorted_members = sorted(members, key=lambda m: m.score, reverse=True)
blocks = {"blocks": [
    {"type": "header", "text": {"type": "plain_text", "text": "Resultater for WoI i Stolpejakten :stolpejakten:"}}]}

for sorted_member in sorted_members:
    section = {
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": f'*{sorted_member.rank}* | {sorted_member.user_name}'
            },
            {
                "type": "mrkdwn",
                "text": f'*{sorted_member.score}*'
            }
        ]
    }
    blocks['blocks'].append(section)

divider = {
    "type": "divider"
}
info = {
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "Om det står NOT FOUND foran navnet dit så betyr det at \ndet dukket opp mer enn én person da jeg "
                "søkte opp navnet ditt.\n Om du bytter til et mer unikt navn, så dukker du også opp :).",
        "emoji": True
    }
}
blocks['blocks'].append(divider)
blocks['blocks'].append(info)

print(blocks)

slack_request = requests.post(url=WEBHOOK_URL, headers={'Content-type': 'application/json'}, data=json.dumps(blocks))

if slack_request.status_code == 200:
    print('Successfully sent slack message')
else:
    print(f'Error[{slack_request.status_code}] sending slack message: {slack_request.text}')
