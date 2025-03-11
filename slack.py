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
    norway_national_day = date(date.today().year, 5, 17)
    title = "Resultater for WoI Stolpejakten :stolpejakten:"
    if date.today() == norway_national_day:
        title = ":flag-no: Resultater for WoI Stolpejakten :flag-no::party_blob:"

    blocks = {"blocks": [{"type": "header", "text": {"type": "plain_text", "text": title}}]}
    has_user_not_found = False
    local_rank = 1
    for sorted_member in sorted_members:
        rank = sorted_member.rank
        local_rank_emoji = ''
        if rank == 'NOT FOUND':
            has_user_not_found = True
        else:
            rank = f'{int(sorted_member.rank):_}'.replace('_', ' ')
            local_rank_emoji = get_placement_emoji(local_rank)
            local_rank += 1
        if sorted_member.rank == 'NOT FOUND':
            has_user_not_found = True
        section = {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f'{local_rank_emoji} [*{rank}*]\t{sorted_member.user_name}'
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
                "text": "Om det står NOT FOUND foran navnet ditt, betyr det enten:\n * Sesongen ikke har startet "
                        "enda.\n * Det dukket opp mer enn én person da navnet ditt ble søkt opp.\n\n"
                        "Bytt til et mer unikt navn om sesongen har startet, så dukker du også opp :).",
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
