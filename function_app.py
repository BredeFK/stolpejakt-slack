import logging
import os

import azure.functions as func
from dotenv import load_dotenv

from slack import format_message, post_slack_message
from stolpejakten import get_group_member_scoreboard

app = func.FunctionApp()

# Get environment variables
load_dotenv()
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
USERNAME = os.environ.get('STOLPEJAKTEN_USERNAME')
PASSWORD = os.environ.get('STOLPEJAKTEN_PASSWORD')
CLIENT_ID = os.environ.get('STOLPEJAKTEN_CLIENT_ID')
GROUP_CODE = os.environ.get('GROUP_CODE')


@app.schedule(schedule="0 0 8 * * 1-5", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    # Stolpejakten requests
    sorted_members = get_group_member_scoreboard(USERNAME, PASSWORD, CLIENT_ID, GROUP_CODE)

    # Slack message formatting
    message = format_message(sorted_members)

    # Post Slack message
    post_slack_message(WEBHOOK_URL, message)
