import os
from dotenv import load_dotenv

from flask import Flask
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from dotenv import load_dotenv

load_dotenv(override=True)

app = Flask(__name__)
slack_token = os.getenv('SLACK_TOKEN')
signing_secret = os.getenv('SLACK_SECRET')

client = WebClient(token=slack_token)
bolt_app= App(token=slack_token,  signing_secret=signing_secret)

handler = SlackRequestHandler(bolt_app)