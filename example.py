# Placeholder

from hypixel import hypixel

API_KEYS = ['API_KEY_HERE_PLS', 'ANOTHER_API_KEY?']
hypixel.setKeys(API_KEYS)

options = ['rank', 'level', 'karma', 'twitter']

while True:
    mahInput = input("\nPlease give me a Minecraft username/UUID: ")
    optionInput = input("Please select from list: {}\n> ".format(options))

    try:
        if optionInput.lower() == "rank":
            player = hypixel.Player(mahInput)
            playerJSON = player.getJSON()
            print("The player is rank: " + player.getRank()['rank'])
            print("Were they previously a staff member? {}".format(player.getRank()['wasStaff']))

        elif optionInput.lower() == "level":
            pass

        elif optionInput.lower() == "karma":
            player = hypixel.Player(mahInput)
            player.getJSON()
            karma = player.JSON['player']['karma']
            print(karma)

        elif optionInput.lower() == "twitter":
            player = hypixel.Player(mahInput)
            player.getJSON()
            try:
                social = player.JSON['player']['socialMedia']
                print(social['TWITTER'])
            except KeyError:
                print("This user doesn't have a Twitter account linked.")
    except hypixel.PlayerNotFoundException:
        print("Cannot find player. :/")