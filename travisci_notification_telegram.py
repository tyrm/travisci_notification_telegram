#!/usr/bin/env python3
"""TravisCI notifier for Telegram.

Program listens for notifications from travis ci and sends them to telegram users."""

import argparse
import configparser
import json
import logging
import time

import coloredlogs
from flask import Flask, request
import telegram
from telegram.error import NetworkError, Unauthorized

coloredlogs.install(level='DEBUG')

parser = argparse.ArgumentParser(description='TravisCI notifier for Telegram')
parser.add_argument("-p", "--port", type=int, help="increase output verbosity", default=8080)
args = parser.parse_args()
logging.debug(args)

config = configparser.ConfigParser()
config.read('config.ini')

if 'telegram' not in config:
    raise KeyError('telegram section not defined in config.ini')

if 'token' not in config['telegram']:
    raise KeyError('token not defined in config.ini/telegram')

bot = telegram.Bot(config['telegram']['token'])

app = Flask(__name__)


@app.route("/travisci/notifications", methods=['POST'])
def hello():
    bot_message = u'👷 Travis CI: {0} Build #{1} {2}\n🐙 {3}/{4} ([{5}-{6}]({7}))\n*{8}:*\n{9}'

    payload = json.loads(request.form['payload'])

    author = payload['author_name']
    branch = payload['branch']
    build_id = payload['number']
    commit_id = payload['commit']
    commit_msg = payload['message']
    compare_url = payload['compare_url']
    repo_owner = payload['repository']['owner_name']
    repo_name = payload['repository']['name']
    status_message = payload['status_message']

    if status_message == 'Passed' or status_message == 'Fixed':
        status_icon = u'🎉'
    elif status_message == 'Broken' or status_message == 'Failed' or status_message == 'Still Failing':
        status_icon = u'❌'
    elif status_message == 'Pending':
        status_icon = u'❔'
    else:
        status_icon = u'⚠️'

    if repo_owner in config and repo_name in config[repo_owner]:
        chat_ids = [x.strip() for x in config[repo_owner][repo_name].split(',')]
        for chat in chat_ids:
            bot.send_message(chat,
                             bot_message.format(status_icon, build_id, status_message, repo_owner,
                                                repo_name, branch, commit_id[:7], compare_url,
                                                author, commit_msg),
                             parse_mode='Markdown')

    return "OK"


def main():
    app.run(port=int(args.port))


if __name__ == "__main__":
    main()
