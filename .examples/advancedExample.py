""" This is an example of how you can use this API to create cool things.
    Just run this and you should see cool stuff. c:"""

import hypixel

API_KEYS = ['API_KEY_HERE_PLS', 'ANOTHER_API_KEY?', 'Etc.']
hypixel.setKeys(API_KEYS) # This sets the API keys that are going to be used.

options = ['rank', 'level', 'karma', 'twitter']

while True:
    mahInput = input("\nPlease give me a Minecraft username/UUID: ")
    optionInput = input("Please select from list: {}\n> ".format(options))
    player = hypixel.Player(mahInput) # Creates a hypixel.Player object using the input.
    try:
        if optionInput.lower() == "rank": # If user selects rank,
            print("The player is rank: " + player.getRank()['rank']) # Get the rank and print it.
            print("Were they previously a staff member? {}".format(player.getRank()['wasStaff']))

        elif optionInput.lower() == "level":
            print("The player is level: " + str(player.getLevel())) # Print the player's low level!

        elif optionInput.lower() == "karma":
            print("The player has {} karma.".format(player.JSON['karma'])) # +25 karma ;)

        elif optionInput.lower() == "twitter": # Okay this is a little more complicated
            try:
                socialMedias = player.JSON['socialMedia']['links'] # Check their social media
                print(socialMedias['TWITTER']) # And if they have a Twitter account, print it.
            except KeyError: # If an error comes up, saying they don't have a twitter account...
                print("This user doesn't have a Twitter account linked.") # Say that.
    except hypixel.PlayerNotFoundException: # If the player doesn't live on earth, catch this exception.
        print("Cannot find player. :/")
