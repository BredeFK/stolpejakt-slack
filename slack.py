import json

import requests


def format_message(sorted_members):
    blocks = {"blocks": [
        {"type": "header", "text": {"type": "plain_text", "text": "Resultater for WoI i Stolpejakten :stolpejakten:"}}]}
    has_user_not_found = False
    for sorted_member in sorted_members:
        if sorted_member.rank == 'NOT FOUND':
            has_user_not_found = True
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

    if has_user_not_found:
        divider = {
            "type": "divider"
        }
        info = {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Om det står NOT FOUND foran navnet ditt, betyr det at \ndet dukket opp mer enn én person da "
                        "jeg søkte opp navnet ditt.\n Om du bytter til et mer unikt navn, så dukker du også opp :).",
                "emoji": True
            }
        }
        blocks['blocks'].append(divider)
        blocks['blocks'].append(info)
    return blocks


def post_slack_message(webhook_url, formatted_message):
    slack_request = requests.post(url=webhook_url, headers={'Content-type': 'application/json'},
                                  data=json.dumps(formatted_message))

    if slack_request.status_code == 200:
        print('Successfully sent slack message')
    else:
        print(f'Error[{slack_request.status_code}] sending slack message: {slack_request.text}')
