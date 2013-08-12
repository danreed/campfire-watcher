import sys
from time import sleep

from camplight import Request, Campfire

from settings import *


campfire_url = 'https://%s.campfirenow.com' % subdomain

request = Request(campfire_url, token)
campfire = Campfire(request)
room = campfire.room(room_name)

# global to track user data so we don't have to requery what we already have
users = {}


def get_user(user_id):
    """
    Gets and sets a user. Returns a user object.
    """
    if user_id in users:
        user = users[user_id]
    else:
        user = campfire.user(user_id)
        users[user_id] = user
    return user


def is_matched(needles, haystack):
    """
    Checks for any of x needles (list of strings) in a haystack (string). If
    any are found it tells us so. This is super simple and doing a basic
    case-insensitive string search.
    """
    if haystack:
        for needle in needles:
            if needle.lower() in haystack.lower():
                return True
    return False


def alert(message):
    """
    Alerts us that one of our match strings has been found in a new message.
    Prints some stuff and sends a system alert beep (OS X only for now).
    This is ripe for expansion. Growl would make sense.
    """
    user = get_user(message['user_id'])
    print '%s - %s' % (user['name'], message['created_at'])
    print '%s\n' % message['body']

    for x in range(0, 5):
        sys.stdout.write('\a')
    sys.stdout.flush()


def watcher(watch_for=[], check_interval=5):
    """
    Watching you watching me. Gets most recent messages from Campfire and
    notifies us if one of our watch strings is present.
    """
    last_id = 0

    while(True):
        recent = room.recent()
        for message in recent:
            if message['id'] > last_id:
                if is_matched(watch_for, message['body']):
                    alert(message)
        last_id = message['id']
        sleep(check_interval)


if __name__ == '__main__':
    if len(watch_for) > 0:
        print '\n\nWatching for: %s\n\n' % ', '.join(watch_for)
        watcher(watch_for, check_interval)
    else:
        print '\n\nI am not watching for anything. So I\'m stopping\n\n'
