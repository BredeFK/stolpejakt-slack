import json
import os

import requests
from dotenv import load_dotenv
from stolpejakten import get_group_member_scoreboard

load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

sorted_members = get_group_member_scoreboard()

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

print(json.dumps(blocks))


def post_slack_message(formatted_message):
    slack_request = requests.post(url=WEBHOOK_URL, headers={'Content-type': 'application/json'},
                                  data=json.dumps(blocks))

    if slack_request.status_code == 200:
        print('Successfully sent slack message')
    else:
        print(f'Error[{slack_request.status_code}] sending slack message: {slack_request.text}')
