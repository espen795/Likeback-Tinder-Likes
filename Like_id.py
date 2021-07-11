import json
import sys, os
import urllib.request
import urllib
import re
from pathlib import Path
import configparser
from datetime import datetime
from random import randint
from time import sleep
from distutils.util import strtobool

# Variables
path = os.path.join(sys.path[0], "pics")
like_path = os.path.join(sys.path[0], "likes")
url_recs = 'https://api.gotinder.com/v2/recs/core'
url_teasers = "https://api.gotinder.com/v2/fast-match/teasers"
like_ids = []
liked_me = []
failed_errors = []
now = datetime.now()


# Def is used to log the errors to a file
def log_to_file(failed_errors):
    with open(os.path.join(sys.path[0], 'errors.log'), 'a') as errorfile:
        for line in failed_errors:
            errorfile.write('{}: {}\n'.format(now.strftime("%m/%d/%Y, %H:%M:%S"), line))
    sys.exit()


# Create config if it doesn't exist
if not os.path.exists(os.path.join(sys.path[0], 'config.ini')):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'remote_mode': 'True', 
        'auto_like_back': 'True', 
        'save_images': 'True', 
        'x_auth': 'PROVIDE X-AUTH TOKEN HERE (see error log how)'
        }

    with open(os.path.join(sys.path[0], 'config.ini'), 'w') as configfile:
        config.write(configfile)


# Read config
config = configparser.ConfigParser()
config.sections()
config.read(os.path.join(sys.path[0], 'config.ini'))

x_auth = config.get('DEFAULT', 'x_auth')

if x_auth.startswith("PROVIDE X-AUTH TOKEN HERE"):
    failed_errors.append('No x-auth provided, you need to edit the x-auth in the config')
    failed_errors.append('Do the following: tinder web -> devtools -> Application -> local storage -> tinder -> APIToken | token might change periodically')
    failed_errors.append('Do not share your token')
    log_to_file(failed_errors)


def like_user(like):
    try:
        url_like = ' https://api.gotinder.com/like/{}'.format(like)
        req = urllib.request.Request(url_like)
        req.add_header('x-auth-token', x_auth)
        data = urllib.parse.urlencode({'s_number': '934744165', 'user_traveling': '0'}).encode()
        resp = urllib.request.urlopen(req, data=data)
        print(resp)
        sleep(randint(1,4)) # try to hide that we are a bot
    except urllib.error.URLError as e:
        failed_errors.append('Failed liking back (no likes?), reason:')
        failed_errors.append(e.reason)
        log_to_file(failed_errors)
            
if failed_errors:
    log_to_file(failed_errors)

userID = input("Enter the user ID to like: ")
pattern = re.compile("[a-z0-9]+")

if pattern.fullmatch(userID) is not None:
    like_user(userID)
else:
    print("Incorrect string format entered")