import json
from datetime import date

import requests


def get_placement_emoji(rank):
    # number emojis from https://www.flaticon.com/packs/numbers-0-to-100-108
    #  medal emojis from https://www.flaticon.com/packs/winning-8
    if rank > 30:
        return rank
    match rank:
        case 1:
            return ':first_place_medal_1:'
        case 2:
            return ':second_place_medal_2:'
        case 3:
            return ':third_place_medal_3:'
        case _:
            return f':number-{rank}:'


def format_message(sorted_members):
    title = "Resultater for WoI Stolpejakten :stolpejakten:"

    blocks = {"blocks": [{"type": "header", "text": {"type": "plain_text", "text": title}}]}
    local_rank = 1
    for sorted_member in sorted_members:
        rank = ':dotted_line_face:'
        local_rank_emoji = ''
        if sorted_member.rank != -1:
            rank = f'{int(sorted_member.rank):_}'.replace('_', ' ')
            rank = f'[*{rank}*]'
            local_rank_emoji = get_placement_emoji(local_rank)
            local_rank += 1
        section = {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f'{local_rank_emoji} {rank}\t{sorted_member.user_name}'
                },
                {
                    "type": "mrkdwn",
                    "text": f'*{sorted_member.score}*'
                }
            ]
        }
        blocks['blocks'].append(section)

    return blocks


def post_slack_message(webhook_url, formatted_message):
    slack_request = requests.post(url=webhook_url, headers={'Content-type': 'application/json'},
                                  data=json.dumps(formatted_message))

    if slack_request.status_code == 200:
        print('Successfully sent slack message')
    else:
        print(f'Error[{slack_request.status_code}] sending slack message: {slack_request.text}')
