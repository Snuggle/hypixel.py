# pylint: disable=C0103
# Simple Hypixel-API in Python, by Snuggle v0.3.2 | 2017-09-29

import json
from random import choice

import requests # TODO: Check that this module is/has been imported.

from hypixel import leveling

HYPIXEL_API_URL = 'https://api.hypixel.net/'

verified_api_keys = []

def setKeys(api_keys):
    for api_key in api_keys:
        response = requests.get(HYPIXEL_API_URL + 'key?key={}'.format(api_key))
        response = json.loads(response.text)
        if response['success'] is True:
            verified_api_keys.append(api_key)
        else:
            print("Error with key.") # TODO/NOTE: Make this more detailed?

class PlayerNotFoundException(Exception):
    pass

class HypixelAPIError(Exception):
    pass

class Player:
    """ This class represents a player on Hypixel as a single object.
        A player has a UUID, a username, statistics etc. """

    JSON = None; UUID = None

    def __init__(self, UUID):
        self.UUID = UUID
        if len(UUID) <= 16: # If the UUID isn't actually a UUID... *rolls eyes* Lazy developers.
            self.getJSON() # Get UUID from Hypixel-API.
            JSON = self.JSON
            uuid = JSON['player']['uuid'] # Pretend that nothing happened.

    def getJSON(self, *args):
        typeOfRequest = 'uuid'
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        UUID = self.UUID
        if len(UUID) <= 16:
            typeOfRequest = 'name'
        response = requests.get(HYPIXEL_API_URL + 'player?key={}&{}={}'.format(api_key, typeOfRequest, UUID))
        response = response.json()
        if response['success'] is True:
            if response['player'] is None:
                raise PlayerNotFoundException(UUID)
            else:
                self.JSON = response
                return response
        else:
            raise HypixelAPIError(response)

    def getPlayerInfo(self):
        JSON = self.JSON
        if JSON is None: # If the player's JSON hasn't been fetched...
            print("\nLookupError: hypixel-python\\Player\\getPlayerInfo: Need to fetch player's JSON data first.")
            raise LookupError
        playerInfo = {}
        playerInfo['uuid'] = self.UUID
        playerInfo['displayName'] = Player.getName(self)
        playerInfo['rank'] = Player.getRank(self)
        playerInfo['networkLevel'] = Player.getLevel(self)
        JSONKeys = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp']
        for item in JSONKeys:
            try:
                playerInfo[item] = JSON['player'][item]
            except KeyError:
                pass
        return playerInfo

    def getName(self):
        JSON = self.JSON
        if JSON is None: # If the player's JSON hasn't been fetched...
            print("\nLookupError: hypixel-python\\Player\\getUsername: Need to fetch player's JSON data first.")
            raise LookupError
        return JSON['player']['displayname']

    def getLevel(self):
        # TODO: Calculate level using global network experience.
        JSON = self.JSON
        if JSON is None: # If the player's JSON hasn't been fetched...
            print("\nLookupError: hypixel-python\\Player\\getLevel: Need to fetch player's JSON data first.")
            raise LookupError
        try:
            networkExp = JSON['player']['networkExp']
        except KeyError:
            networkExp = 0
        try:
            networkLevel = JSON['player']['networkLevel']
        except KeyError:
            networkLevel = 0
        exp = leveling.getExperience(networkExp, networkLevel)
        myoutput = leveling.getExactLevel(exp)
        return myoutput
        
    def getRank(self):
        """ This function returns a player's rank, from their data. """
        JSON = self.JSON
        if JSON is None: # If the player's JSON hasn't been fetched...
            print("\nLookupError: hypixel-python\\Player\\getRank: Need to fetch player's JSON data first.")
            raise LookupError
        playerRank = {} # Creating dictionary.
        playerRank['wasStaff'] = False
        possibleRankLocations = ['packageRank', 'newPackageRank', 'rank']

        for Location in possibleRankLocations:
            if Location in JSON['player']:
                if Location == 'rank' and JSON['player'][Location] == 'NORMAL':
                    playerRank['wasStaff'] = True
                else:
                    dirtyRank = JSON['player'][Location].title()
                    dirtyRank = dirtyRank.replace("_", " ").replace("Mvp", "MVP").replace("Vip", "VIP") # pylint: disable=line-too-long
                    playerRank['rank'] = dirtyRank.replace(" Plus", "+")

        if 'rank' not in playerRank:
            playerRank['rank'] = 'Non'

        return playerRank

    def getGuildID(self):
        UUID = self.UUID
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        response = requests.get(HYPIXEL_API_URL + 'findGuild?key={}&byUuid={}'.format(api_key, UUID))
        response = response.json()
        if response['success'] is True:
            return response['guild']
        else:
            raise HypixelAPIError(response)

class Guild:
    GuildID = None
    def __init__(self, GuildID):
        if len(GuildID) == '24':
            self.GuildID = GuildID

    def getJSON(self):
        GuildID = self
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        response = requests.get(HYPIXEL_API_URL + 'guild?key={}&id={}'.format(api_key, GuildID))
        response = response.json()
        if response['success'] is True:
            return response
        else:
            raise HypixelAPIError(response)