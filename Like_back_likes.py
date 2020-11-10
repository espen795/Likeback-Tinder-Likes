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
like_ids_clean = []
liked_me = []
failed_errors = []
now = datetime.now()
runs = 3

remote_mode = None
auto_like_back = None
save_images = None
x_auth = None
refresh_token = None

# Def is used to log the errors to a file
def log_to_file(failed_errors):
    with open(os.path.join(sys.path[0], 'errors.log'), 'a') as errorfile:
        for line in failed_errors:
            errorfile.write('{}: {}\n'.format(now.strftime("%m/%d/%Y, %H:%M:%S"), line))
    sys.exit()


# Used to get json data from the (tinder) url profided
def get_data(url):
    req = urllib.request.Request(url)
    req.add_header('x-auth-token', x_auth)
    resp = urllib.request.urlopen(req)
    content = resp.read()
    return json.loads(content)


# Is used to get a profile based on the id provided
def get_profile(tinder_id):
    profile_url = "https://api.gotinder.com/user/{}".format(tinder_id)
    response = get_data(profile_url)
    file_name = '{}.txt'.format(tinder_id)

    with open(os.path.join(like_path, file_name), 'w') as userfile:
        userfile.write(json.dumps(response, indent=4, sort_keys=True))


# Create config if it doesn't exist
def create_config():
    if not os.path.exists(os.path.join(sys.path[0], 'config.ini')):
        print("Creating config")
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'remote_mode': 'True', 
            'auto_like_back': 'True', 
            'save_images': 'True', 
            'refresh_token': 'None',
            'x_auth': 'None'
            }

        with open(os.path.join(sys.path[0], 'config.ini'), 'w') as configfile:
            config.write(configfile)


# Setup all required config items
def ready_settings():
    create_config()
    print("Reading settings from config")
    
    # Read config
    config = configparser.ConfigParser()
    config.sections()
    config.read(os.path.join(sys.path[0], 'config.ini'))

    global remote_mode
    remote_mode = strtobool(config.get('DEFAULT', 'remote_mode'))
    global auto_like_back
    auto_like_back = strtobool(config.get('DEFAULT', 'auto_like_back'))
    global save_images
    save_images = strtobool(config.get('DEFAULT', 'save_images'))
    global x_auth
    x_auth = config.get('DEFAULT', 'x_auth')
    global refresh_token
    refresh_token = config.get('DEFAULT', 'refresh_token')

    if refresh_token.startswith("None"):
        print("No refresh_token token found")
        failed_errors.append('No refresh_token provided, you need to edit the refresh_token in the config')
        failed_errors.append('Do the following: tinder web -> devtools -> Application -> local storage -> tinder -> refresh token')
        failed_errors.append('Do not share your token')
        log_to_file(failed_errors)

    # Test if pics folder exists, if not create
    if save_images or not remote_mode:
        Path(path).mkdir(parents=True, exist_ok=True)

    # Test if pics folder exists, if not create
    if not auto_like_back:
        Path(like_path).mkdir(parents=True, exist_ok=True)


# Using the refresh_token to get a new api_token
def authenticate():
    try:
        req = urllib.request.Request('https://api.gotinder.com/v2/auth/login/sms')

        data = {'refresh_token': refresh_token}
        resp = urllib.request.urlopen(req, data=json.dumps(data).encode('utf-8'))
        
        print("Getting new api token: ", resp.status)

        content = resp.read()
        cont = json.loads(content)
        data = cont['data']
        global x_auth
        x_auth = data['api_token']
        
        config = configparser.ConfigParser()
        config.sections()
        config.read(os.path.join(sys.path[0], 'config.ini'))
        config.set('DEFAULT', 'x_auth', x_auth)

        # Writing our configuration file
        with open(os.path.join(sys.path[0], 'config.ini'), 'w') as configfile:
            config.write(configfile)

        print("Saved new token and continuing the program...")
    except urllib.error.URLError as e:
        print("Failed getting new API token, see error log")
        failed_errors.append('Failed getting new api token, reason: ' + e.reason)
        log_to_file(failed_errors)



# Test the connection to Tinder, on exeption a new token is requested
def test_conn():
    try:
        print("Testing connection to API: ", end="")
        req = urllib.request.Request(url_teasers)
        req.add_header('x-auth-token', x_auth)
        resp = urllib.request.urlopen(req)
        print(resp.status)
    except urllib.error.URLError as e:
        if e.reason.find("401"):
            print("auth token invalid... Trying to obtain a new one")
            authenticate()
        else:
            print("other error see error log")
            failed_errors.append('Failed getting likes, reason: ' + e.reason)
            log_to_file(failed_errors)



# Script supports running from the pics folder aswel to include extra likes
def get_teasers_remote():
    try:
        response = get_data(url_teasers)
        print("Got teasers from remote")

        data = response['data']
        results = data['results']

        i = 0
        if save_images:
            print("Searching for likes and saving them, found:")
        else:
            print("Searching for likes, found:", end="")

        for users in results:
            user = users['user']
            photo = user['photos']
            elist2 = photo[0]
            url = elist2['url']
            filename = url.split('/')[-1]

            if save_images:
                urllib.request.urlretrieve(url, os.path.join(sys.path[0], "pics/", filename))
            
            if re.search('_(.*)_(.*)\.', filename):
                result = re.findall('.*_(.*)\.', filename)
            else:
                result = re.findall('_(.*)\.', filename)
            if result:
                print(i, " ", end="")
                liked_me.append(result)
                i += 1
        print()
    except urllib.error.URLError as e:
        failed_errors.append('Failed getting likes, reason: ' + e.reason)
        log_to_file(failed_errors)


# If the system is running in local mode (for whatever reason) we can get the teaser ids from the image names
def get_teasers_local():
    print("Running in offline mode")
    for root, directories, files in os.walk(path):
        for file in files:
            if re.search('_(.*)_(.*)\.', file):
                result = re.findall('.*_(.*)\.', file)
            else:
                result = re.findall('_(.*)\.', file)
            if result:
                print("Found a like")
                liked_me.append(result)


# Getting a list of users and checking if they liked you
def get_likes_from_teaser():
    print("Trying to find likes in recommended profiles")
    try:
        response = get_data(url_recs)
        data = response['data']

        if 'results' in data:
            results = data['results']
        
            for users in results:
                user = users['user']
                photo = user['photos']
                elist2 = photo[0]
                url = elist2['url']    

                if re.search('_(.*)_(.*)\.', url):
                    result = re.findall('.*_(.*)\.', url)
                else:
                    result = re.findall('_(.*)\.', url)

                for like in liked_me:
                    if like == result:
                        print("Found the profile ID of someone who liked you: ", user["_id"])
                        like_ids.append(user["_id"])
        else:
                print("There are no profiles returned by Tinder, try changing your search distance")
                failed_errors.append('There are no profiles returned by Tinder')
                log_to_file(failed_errors)

    except urllib.error.URLError as e:
        failed_errors.append('Failed getting recs from tinder, reason:')
        failed_errors.append(e.reason)
        log_to_file(failed_errors)


# Liking the users back or print their id to a file
def like_back(like):
    try:
        url_like = ' https://api.gotinder.com/like/{}'.format(like)
        req = urllib.request.Request(url_like)
        req.add_header('x-auth-token', x_auth)
        data = urllib.parse.urlencode({'s_number': '12345678', 'user_traveling': '0'}).encode()
        resp = urllib.request.urlopen(req, data=data)
        print("Liking profile back: ", like, resp.status)
        
        # try to hide that we are a bot
        sleep(randint(1,4)) 
    except urllib.error.URLError as e:
        failed_errors.append('Failed liking back (no likes?), reason:')
        failed_errors.append(e.reason)
        log_to_file(failed_errors)


# Main executes the code
def main():
    test_conn()

    if remote_mode:
        get_teasers_remote()
    else:
        get_teasers_local()
        
    for x in range(runs):
        print("Run:",x+1 , "of", runs)
        get_likes_from_teaser()

    if not like_ids:
        print("\nCouldn't find likes  :(")
    else:
        print("\nRemoving duplicates from like list...")

        like_ids_clean = set([x for x in like_ids if like_ids.count(x) > 0])

        for like in like_ids_clean:
            if auto_like_back:
                like_back(like)
            else:
                get_profile(like)

    if failed_errors:
        print("Finished with errors, see log")
        log_to_file(failed_errors)

# Run the actual program
ready_settings()

main()
sleep(4)