# Likeback-Tinder-Likes
A script to like back your Tinder likes using (or in this context abusing) the teasers function in Tinder.
The script allows you to utilise some gold functionality without the actual subscription. It is therefore intended for educational purposes (please don't sue me Tinder)

Small footnote because I have already got this question from friends:
1) You can only like back people who liked you (of course)
2) You have not swiped on (neither liked or disliked) them yet. Tinder does sometimes show profiles again, but this is rare and random.
3) You might need to manually remove pictures from the pics folder
4) Tinder only serves you the 10 most recent likes with the teasers function. Using local mode might help with this.



<h2>FIRST STEPS BEFORE RUNNING</h2>

Download Python: https://www.python.org/downloads/
Install Python

You need to get your API (refresh) token. The easiest way is through Tinderweb. The example is for Chrome, the steps for other browsers might differ slightly.
1. Go to https://tinder.com/
1. Press F12
1. Navigate to tab Application
1. Look for Storage -> Local Storage and click on the Tinder URL
1. Find and copy the value for the TinderWeb/LoginDataRefreshToken (DON'T SHARE THIS CODE WITH ANYONE!)
    1. No refresh token: copy the APIToken instead
1. Run the script for the first time
1. Open the config.ini
1. Paste the code after refresh_token = {CODE-GOES-HERE}
    1. No refresh token: put text into refresh_token = abcdef 
    1. No refresh token: paste APIToken into x_auth = {CODE-GOES-HERE}
    1. Note: API token will not remain valid for long, only give or take a day


<h2>CHANGING THE SETTINGS</h2>

The following stettings are available:
1) remote_mode 
        True = get the most recent teasers from Tinder
        False = run using the filenames in the pics folder (as this might contain older profiles)
2) auto_like_back, speaks for itself right
3) save_images, if true save in the pics folder
4) refresh_token = the code you pasted in first install
5) x_auth = used to authenticate


<h2>Sources</h2>
Got the api information from https://github.com/fbessez/Tinder

<h2>Development</h2>
Developing on this script is difficult, because I need to get (sometimes multiple) likes. Not always easy.

<h3>Not tested</h3>
-

<h3>Feature improvements</h3>
Authentication using cookies.

Creating a combined mode where both local storage and remote mode is used.

Some functionality to allow user to actually view a profile before liking back.

Customise amount of tries per run in config.

Send automatic message when matched using customised string, ex: "Hey %name, how are you doing?".


<h3>Bugs</h3>
The LoginDataRefreshToken variable is not always available. It looks like sometimes the browser authenticates using a cookie. I will look into this, and try implementing cookie authentication.
Please inform me if there are any!
