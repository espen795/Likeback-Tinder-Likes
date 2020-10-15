# Likeback-Tinder-Likes
A script to like back your Tinder likes using (or in this context abusing) the teasers function in Tinder.
The script allows you to utilise some gold functionality without the actual subscription. It is therefore intended for educational purposes (please don't sue me Tinder)

Small footnote because I have already got this question from friends:
1) You can only like back people who liked you (of course)
2) You have not swiped on (neither liked or disliked) them yet. Tinder does sometimes show profiles again, but this is rare and random.
3) You might need to manually remove pictures from the pics folder



<h2>FIRST STEPS BEFORE RUNNING</h2>

Download Python: https://www.python.org/downloads/
Install Python

You need to get your API refresh token. The easiest way is through Tinderweb. The example is for Chrome, the steps for other browsers might differ slightly.
1) Go to https://tinder.com/
2) Press F12
3) Navigate to tab Application
4) Look for Storage -> Local Storage and click on the Tinder URL
5) Find and copy the value for the TinderWeb/LoginDataRefreshToken (DON'T SHARE THIS CODE WITH ANYONE!)
6) Run the script for the first time
7) Open the config.ini
8) paste the code after refresh_token = XXXXXXXX-CODE-GOES-HERE-XXXXXXXXXX 



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
I recently added line 282 and like_ids_clean to remove duplicate profile IDs. This functionality is not yet tested.

<h3>Feature improvements</h3>
Creating a combined mode where both local storage and remote mode is used.
Some functionality to allow user to actually view a profile before liking back

<h3>Bugs</h3>
None that I am aware of
