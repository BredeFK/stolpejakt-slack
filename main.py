import os

from dotenv import load_dotenv
from stolpejakten import get_group_member_scoreboard
from slack import format_message, post_slack_message

# Get environment variables
load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
USERNAME = os.environ.get('STOLPEJAKTEN_USERNAME')
PASSWORD = os.environ.get('STOLPEJAKTEN_PASSWORD')
CLIENT_ID = os.environ.get('STOLPEJAKTEN_CLIENT_ID')
GROUP_CODE = os.environ.get('GROUP_CODE')

# Stolpejakten requests
sorted_members = get_group_member_scoreboard(USERNAME, PASSWORD, CLIENT_ID, GROUP_CODE)

# Slack message formatting
message = format_message(sorted_members)

# Post Slack message
post_slack_message(WEBHOOK_URL, message)
