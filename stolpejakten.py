import urllib.parse

import requests

from Member import Member

BASE_URL = 'https://apiv10.stolpejakten.no'


def get_group_id(token, group_code):
    req_me = requests.get(url=f'{BASE_URL}/affiliations/me', headers={'Authorization': f'Bearer {token}'})
    if req_me.status_code == 200:
        user_groups = req_me.json()
        if len(user_groups['results']) != 0:
            group_id = None
            for group in user_groups['results']:
                if group['code'] == group_code:
                    group_id = group['id']
            if group_id is None:
                print(f'Error: Group with code {group_code} not found')
            else:
                print(f'Group with code {group_code} found')
                return group_id
        else:
            print(f'Error: user has no groups')
    else:
        print(f'Error getting group ID: {req_me.status_code}: {req_me.text}')
        return None


def get_group_member_names(token, group_code):
    group_id = get_group_id(token, group_code)
    if group_id is None:
        exit("Error: GroupId not found")

    req_group = requests.get(url=f'{BASE_URL}/affiliations/members/{group_id}',
                             headers={'Authorization': f'Bearer {token}'})
    if req_group.status_code == 200:
        group_members = req_group.json()
        if len(group_members['results']) != 0:
            name_list = []
            for member in group_members['results']:
                name_list.append(member['name'])
            print(f'Found {len(group_members["results"])} members')
            return name_list
        else:
            print(f'Error: Could not find members for group {group_id}')
            return None
    else:
        print(f'Error getting members for group {group_id}: {req_group.status_code}: {req_group.text}')
        return None


def get_group_member_scoreboard(token, group_code):
    member_names = get_group_member_names(token, group_code)
    if member_names is None:
        exit("Error: Group members not found")

    members = []
    for name in member_names:
        urlencoded_name = urllib.parse.quote_plus(name)
        req_user = requests.get(
            url=f'{BASE_URL}/toplists?type=-1&kommune=0&page=0&search={urlencoded_name}',
            headers={'Authorization': f'Bearer {token}'})

        if req_user.status_code == 200:
            body = req_user.json()
            if body['count'] == 1:
                user = body['results'][0]
                member = Member(user['rank'], user['user_name'], int(user['score']))
                members.append(member)
            else:
                members.append(Member('NOT FOUND', name, -1))
                print(f'Found more than one user with name {name}')
        else:
            print(f'Something went wrong: {req_user.status_code}: {req_user.text}')
            return None

    return sorted(members, key=lambda m: m.score, reverse=True)
