### Bot.py
# Bot:
- Adds every user to an sql3 database file and work with their info.
- Has an xp system, which means, that user will get an amount of xp after every message he sends and get a new level, when the amounts xp he has equals or exceeds the valu
he need to get a rank up. After every rank uo bot will send a congratulations to a user.
- If the message has in it the secret phrase, bot will give a secret role to user, that send this message and will take it off after 30 minutes.
- Has moderator functions in moder.py. It means, that it will check each message for
banned words and punnish users for using them. Or encourage.
- Gives a role if user used an emoji on message. You can use it to give users nececery roles when they join the server only by leaving an emoji on message.
# ON_READY
```py
def on_ready
#Called when the client is done preparing the data received from Discord.
#In my code after bot login in it calls func named 'userdata
```
# ON_MESSAGE
```py
def on_message
#Called when server member writes a messagge in channel bot have rights to read
#After message is send bot checks the author of messae and if it hasn`t been send by himself, it will call 'onmessagge' func drom defmodule file.
```
Methods:
```
message
```
# IN_RAW_REACTIOIN_ADD
```py
def on_raw_reaction_add
#Called when an emoji has been used on message.
```
Methods:
```
payload
```
# Defmodule.py
Defmodule - module that contains all the functions bot uses. This module has been created to clean the main code from not nececery functions.
Functions:
```
def is_record_exists
def userdata
def reactionrole
def onmessage
```
# is_record_exists
This function checks the whole db file and takes all user_id it contains.
# userdata
This function is the biggest and the most important func in whole code.
As first, this finction creating a list of users that are on server and checks against thedatabase. 
If user is in server but has no personal record in db file, bot creates this record, gives to user the role and continues to work with user. 
Elsif user has a record, but he is not on server, the record getting deleted bu bot. 
And if user has a record and he is on server, he just gets the role. If user already has the role, bot does not looks for him in db file to not waste time.
# reactiinrole
This  function called when on_raw_reaction_add got called. If the message the emoji was used on is a target_message, user gets the role.
# onmessage
This function called after every users message. After every message user gets 3 xp and its immediately adds to amount xp he already has.
After it the func checks, does user has enough xp to get a new lvl. If user has, that bot sends him message about new lvl, adds in db file to user_lvl 1 and sets the value of user xp to 0. 
If not bot just does nothing with users lvl. After it bot looks for a secret phrase in massage and if he finds it, he gives the user role for 30 minutes.
