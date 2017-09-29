# pylint: disable=C0103
# Simple Hypixel-API in Python, by Snuggle v0.3 | 2017-09-29

import json
from random import choice

import requests # TODO: Check that this module is/has been imported.

HYPIXEL_API_URL = 'https://api.hypixel.net/'
SKIN_API_URL = 'https://visage.surgeplay.com/' # NOTE: Not sure if this'll be kept.

verified_api_keys = []

def setKeys(api_keys):
    for api_key in api_keys:
        response = requests.get(HYPIXEL_API_URL + 'key?key={}'.format(api_key))
        response = json.loads(response.text)
        if response['success'] is True:
            verified_api_keys.append(api_key)
        else:
            print("Error with key.") # TODO/NOTE: Make this more detailed?

class Player:
    """ This class represents a player on Hypixel as a single object.
        A player has a UUID, a username, statistics etc. """

    playerJSON = None; playerUUID = None

    def __init__(self, playerUUID):
        self.playerUUID = playerUUID
        if len(playerUUID) <= 16:
            print("This is a username, not a UUID. Not implemented yet.")
            raise NotImplementedError
        # TODO: Check if it's a UUID. If not, display warning and convert to a UUID.

    def getJSON(self):
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        playerUUID = self.playerUUID
        response = requests.get(HYPIXEL_API_URL + 'player?key={}&uuid={}'.format(api_key, playerUUID))
        response = response.json()
        self.playerJSON = response
        return response

    def getPlayerInfo(self):
        # TODO: Return a dictionary of basic player information. {uuid: 'xxx', username: 'Snuggle', networkLevel: '32'}
        print("test")

    def getUsername(self):
        # TODO: Convert UUID to player-name.
        raise NotImplementedError

    def getLevel(self):
        # TODO: Calculate level using global network experience.
        raise NotImplementedError

    def getRank(self):
        playerJSON = self.playerJSON
        if playerJSON is None:
            print("\nLookupError: hypixel-python\\getRank: Need to fetch player's JSON data first.")
            raise LookupError
        playerRank = {} # Creating dictionary.
        playerRank['wasStaff'] = False
        possibleRankLocations = ['packageRank', 'newPackageRank', 'rank']

        for Location in possibleRankLocations:
            if Location in playerJSON['player']:
                if Location == 'rank' and playerJSON['player'][Location] == 'NORMAL':
                    playerRank['wasStaff'] = True
                else:
                    dirtyRank = playerJSON['player'][Location].title()
                    dirtyRank = dirtyRank.replace("_", " ").replace("Mvp", "MVP").replace("Vip", "VIP") # pylint: disable=line-too-long
                    playerRank['rank'] = dirtyRank.replace(" Plus", "+")

        return playerRank

    def getSkinRender(self, size):
        # FIXME/TODO/XXX - Don't run this.
        playerUUID = self.playerUUID
        url = 'https://visage.surgeplay.com/full/{}/{}'.format(size, playerUUID)
        return url
