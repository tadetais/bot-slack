import os
from flask import request
from slack_sdk.errors import SlackApiError
from reports.reports import init
from config import app, client, bolt_app, handler

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
    mode = {"dev": True, "prod": False}
    app.run(host="0.0.0.0", port=os.getenv("APP_PORT"), debug=mode.get(os.getenv("APP_ENV", False)))