# Likeback-Tinder-Likes
A script to like back your Tinder likes using (or in this contect abusing) the teasers function in Tinder.

Small footnote because I have already got this question from friends, you can only like back people who:
1) Liked you (ofcourse)
2) You have not swiped on (neither liked or disliked). Tinder does sometimes show profiles again, but this is rare and random.
3) Developing on this script is difficult, because I need to get (sometimes multiple) likes. Not always easy.
4) You might need to manually remove pictures from the pics folder



<h2>FIRST STEPS BEFORE RUNNING</h2>

Download Python: https://www.python.org/downloads/
Install Python

You need to get your API refresh token. The easiest way is through Tinderweb.
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
