import os

from flask import Flask, request
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SLACK_SECRET')

client = WebClient(token=slack_token)
bolt_app = App(token=slack_token,  signing_secret=signing_secret)

handler = SlackRequestHandler(bolt_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@bolt_app.message("olá bot")
def responde_teste(payload: dict, say: Say):
    user = payload.get('user')
    print(user)
    say(f"Olá <@{user}>")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)