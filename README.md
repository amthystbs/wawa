# wawa documentation

### Usage for players
One person starts by saying "a", then someone says "wa", then someone says "awa", then "wawa", "awawa", "wawawa", etc.
The same user cannot send a wawa twice in a row.

### Commands
- /enable_wawa - Enables the bot in the channel you're currently in. Can only be run by admins.
- /disable_wawa - Disables the bot in the channel you're currently in, and deletes all of the current channel's saved data from the wawa server. May be changed later.
- /reset_channel - Resets all data from the wawa bot in the channel you're currently in.
- /show_record - Shows the current record wawa length achieved in your current channel.
- /reset_record - Resets the record in your current channel.
- /set_reaction - Sets the reaction of your choosing to an emoji chosen in the "symbol" field. Leaving the "symbol" field blank makes it so there isn't a reaction. Note that if the input you use in "symbol" isn't a valid discord reaction, it will default to showing nothing.
- /reset_reaction - Resets the reaction of your choosing to the default, also allows you to select "all" to reset all of them.
- /list_reactions - Generates a list of all the reactions currently being used in the channel.

### Self hosting the bot
To run this bot yourself, create a file called .env in the folder you plan to run it in and write 
`DISCORD_TOKEN = [The token of the discord bot you want to use]`
The discord bot requires all 3 priveledged intents as well as the View Channels, Send Messages, and Add Reactions permissions. 
This bot is only intended to be installed on Guilds and not for individual users.
