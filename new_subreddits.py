import time
import requests
import json
import os
import sys

firstRun = True
subreddits = []
new_subreddits = []

reddit_url = 'http://reddit.com/subreddits/new.json'
headers = {
    'User-Agent': 'Python testing for u/{}'.format(os.getenv('REDDIT_USERNAME', 'random_person'))
}

enable_alerts_env = os.getenv('ENABLE_PUSHOVER', 'false')
enable_alerts = False if enable_alerts_env.lower() in ['false', 'no'] else True
pushover_url = 'https://api.pushover.net/1/messages.json'
pushover_token = os.getenv('PUSHOVER_TOKEN', None)
pushover_user = os.getenv('PUSHOVER_USER', None)


def alert() :
    if not enable_alerts:
        return True
    if pushover_token and pushover_user and len(new_subreddits) > 0:
        message = ''
        for sub in new_subreddits:
            message += "  -  %s %s \n" % (sub['id'], sub['name'])

        payload = {'token': pushover_token, 'user': pushover_user, 'message': message, 'title': 'New Subreddits'}
        r = requests.post(pushover_url, data=payload)
        if r.status_code == 200:
            print("Notification sent!", file=sys.stdout)


def monitor() :
    r = requests.get(reddit_url, headers=headers)
    subs = r.json()['data']['children']

    for subreddit in subs:
        data = subreddit['data']
        sub_id = data['id']
        display_name = data['display_name']
        if len(display_name) == 0:
            continue

        if len(sub_id) == 0:
            continue


        sub_dict = {'id': sub_id, 'name': display_name}
        if sub_dict not in subreddits:
            subreddits.append(dict(sub_dict))
            new_subreddits.append(dict(sub_dict))


if __name__ == '__main__':
    while True:
        monitor()

        if firstRun:
            firstRun = False
            del new_subreddits[:]
            print('The script just started... I am gathering information, please wait.', file=sys.stdout)
            print('-' * 10, file=sys.stdout)
            print("New Subreddits since script started:", file=sys.stdout)
            continue

        if len(new_subreddits) > 0:
            for sub in new_subreddits:
                print(" - %s %s" % (sub['id'], sub['name']), file=sys.stdout)
            alert()
            del new_subreddits[:]

        time.sleep(60)
