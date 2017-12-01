""" This is an example of how you can use this API to create cool things.
    Just run this and you should see cool stuff. c:"""

import hypixel

API_KEYS = ['API_KEY_HERE_PLS']
hypixel.setKeys(API_KEYS) # This sets the API keys that are going to be used.

Player = hypixel.Player('Snuggle') # This creates a Player-object and puts it to a variable called "Player".

PlayerName = Player.getName() # This gets the player's name and puts it in a variable called "PlayerName". :3
print("Player is called ", end='')
print(PlayerName)

PlayerLevel = Player.getLevel()
print(PlayerName + " is level: ", end='')
print(PlayerLevel) # This prints the level that we got, two lines up!

PlayerRank = Player.getRank()
print(PlayerName + " is rank: ", end='')
print(PlayerRank['rank'])