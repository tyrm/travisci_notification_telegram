# travisci_notification_telegram
TravisCI notifier for Telegram.

listens by default on http://0.0.0.0:8080/travisci/notifications

## Configuration
###config.ini
```INI
[telegram]
token=123456789:AbCdEfGhIjKlMnOpQrStU-vWxYz12345678

# Send notifications for all repos for githubuser1 to chat_id 123456
[githubuser1]
*=123456

[githubuser2]
# Send notifications for repo-a for githubuser2 to chat_id -123456
repo-a=-123456
# Send notifications for repo-b for githubuser2 to chat_id 123456 and 98765
repo-b=123456,98765
```

## Running
usage: travisci_notification_telegram.py [-h] [-p PORT] [-H HOST]

TravisCI notifier for Telegram

optional arguments:
* -h, --help            show this help message and exit
* -p PORT, --port PORT  listening port of notifier
* -H HOST, --host HOST  listening hostname of notifier
