import logging
import os

import azure.functions as func

from slack import format_message, post_slack_message
from stolpejakten import get_group_member_scoreboard

app = func.FunctionApp()


@app.schedule(schedule="0 0 6 * * Mon", arg_name="myTimer", run_on_startup=False,
              use_monitor=True)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    # Get environment variables
    WEBHOOK_URL = os.environ["WEBHOOK_URL"]
    USERNAME = os.environ["STOLPEJAKTEN_USERNAME"]
    PASSWORD = os.environ["STOLPEJAKTEN_PASSWORD"]
    CLIENT_ID = os.environ["STOLPEJAKTEN_CLIENT_ID"]
    GROUP_CODE = os.environ["GROUP_CODE"]

    logging.info('Python timer trigger function executed.')
    # Stolpejakten requests
    sorted_members = get_group_member_scoreboard(USERNAME, PASSWORD, CLIENT_ID, GROUP_CODE)

    # Slack message formatting
    message = format_message(sorted_members)

    # Post Slack message
    post_slack_message(WEBHOOK_URL, message)
