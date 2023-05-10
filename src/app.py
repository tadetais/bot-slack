import os
import sys

from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt import App, Say, Ack
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv
from reports.reports import init

load_dotenv(override=True)

app = Flask(__name__)
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SLACK_SECRET')

client = WebClient(token=slack_token)
bolt_app= App(token=slack_token,  signing_secret=signing_secret)

handler = SlackRequestHandler(bolt_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@bolt_app.message("status")
def get_card_status(payload: dict):
    try:
        id_card = int(payload.get('text')[7:])
        info = init(id_card, payload["user"])

        client.chat_postMessage(
            channel=payload.get('channel'),
            thread_ts=payload.get('ts'),
            blocks=info
        )

    except SlackApiError as e:
        print(e.response["error"])



if __name__ == '__main__':
    mode = False if sys.argv[1] != "dev" else True
    app.run(host="0.0.0.0", port="8888", debug=mode)