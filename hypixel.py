""" Simple Hypixel-API in Python, by Snuggle v0.4.2 | 2017-09-30 to 2017-10-03 """
# pylint: disable=C0103
# TODO: Add more comments, saying what is happening. :p

import json
from random import choice
import requests

import leveling

HYPIXEL_API_URL = 'https://api.hypixel.net/'
MOJANG_SESSION_SERVER_URL = "https://sessionserver.mojang.com/session/minecraft/profile/"

HYPIXEL_API_KEY_LENGTH = 36 # This is the length of a Hypixel-API key. Don't change from 36.
verified_api_keys = []

class PlayerNotFoundException(Exception):
    """ Simple exception if a player/UUID is not found. """
    pass

class HypixelAPIError(Exception):
    """ Simple exception if something's gone very wrong. Usually incorrect API keys. """
    pass

def setKeys(api_keys):
    """ This function is used to set your Hypixel API keys.
        It also checks that they are valid/working. """
    for api_key in api_keys:
        if len(api_key) == HYPIXEL_API_KEY_LENGTH:
            response = requests.get(HYPIXEL_API_URL + 'key?key={}'.format(api_key))
            response = json.loads(response.text)
            if response['success'] is True:
                verified_api_keys.append(api_key)
            else:
                raise HypixelAPIError("hypixel/setKeys: Error with key XXXXXXXX-XXXX-XXXX-XXXX{} | {}".format(api_key[23:], response))
        else:
            raise HypixelAPIError("hypixel/setKeys: The key '{}' is not 36 characters.".format(api_key))

class Player:
    """ This class represents a player on Hypixel as a single object.
        A player has a UUID, a username, statistics etc. """

    JSON = None
    UUID = None

    def __init__(self, UUID):
        """ This is called whenever someone uses hypixel.Player('Snuggle').
            Get player's UUID, if it's a username. Get Hypixel-API data. """
        self.UUID = UUID
        self.getJSON() # Get player's Hypixel-API JSON information.
        if len(UUID) <= 16: # If the UUID isn't actually a UUID... *rolls eyes* Lazy people.
            JSON = self.JSON
            self.UUID = JSON['uuid'] # Pretend that nothing happened and get the UUID from the API.

    def getJSON(self):
        """ This function is used for getting JSON from Hypixel's Public API. """
        UUIDType = 'uuid'
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        UUID = self.UUID
        if len(UUID) <= 16:
            UUIDType = 'name'
        response = requests.get(HYPIXEL_API_URL + \
                                'player?key={}&{}={}'.format(api_key, UUIDType, UUID))
        response = response.json()
        if response['success'] is True:
            if response['player'] is None:
                raise PlayerNotFoundException(UUID)
            else:
                self.JSON = response['player']
        else:
            raise HypixelAPIError(response)

    def getPlayerInfo(self):
        """ This is a simple function to return a bunch of common data about a player. """
        JSON = self.JSON
        playerInfo = {}
        playerInfo['uuid'] = self.UUID
        playerInfo['displayName'] = Player.getName(self)
        playerInfo['rank'] = Player.getRank(self)
        playerInfo['networkLevel'] = Player.getLevel(self)
        JSONKeys = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp']
        for item in JSONKeys:
            try:
                playerInfo[item] = JSON[item]
            except KeyError:
                pass
        return playerInfo

    def getName(self):
        """ Just return player's name. """
        JSON = self.JSON
        return JSON['displayname']

    def getLevel(self):
        """ This function calls leveling.py to calculate a player's network level. """
        JSON = self.JSON
        try:
            networkExp = JSON['networkExp']
        except KeyError:
            networkExp = 0
        try:
            networkLevel = JSON['networkLevel']
        except KeyError:
            networkLevel = 0
        exp = leveling.getExperience(networkExp, networkLevel)
        myoutput = leveling.getExactLevel(exp)
        return myoutput

    def getRank(self):
        """ This function returns a player's rank, from their data. """
        JSON = self.JSON
        playerRank = {} # Creating dictionary.
        playerRank['wasStaff'] = False
        possibleRankLocations = ['packageRank', 'newPackageRank', 'rank']

        for Location in possibleRankLocations:
            if Location in JSON:
                if Location == 'rank' and JSON[Location] == 'NORMAL':
                    playerRank['wasStaff'] = True
                else:
                    dirtyRank = JSON[Location].title()
                    dirtyRank = dirtyRank.replace("_", " ").replace("Mvp", "MVP").replace("Vip", "VIP") # pylint: disable=line-too-long
                    playerRank['rank'] = dirtyRank.replace(" Plus", "+")

        if 'rank' not in playerRank:
            playerRank['rank'] = 'Non'

        return playerRank

    def getGuildID(self):
        """ This function is used to get a GuildID from a player. """
        UUID = self.UUID
        api_key = choice(verified_api_keys) # Select a random API key from those available.
        response = requests.get(HYPIXEL_API_URL + \
                            'findGuild?key={}&byUuid={}'.format(api_key, UUID))
        response = response.json()
        if response['success'] is True:
            return response['guild']
        else:
            raise HypixelAPIError(response)

    def getSession(self):
        """ This function is used to get a player's session information. """
        UUID = self.UUID
        api_key = choice(verified_api_keys) # Select a random API key from those available.
        response = requests.get(HYPIXEL_API_URL + \
                            'session?key={}&uuid={}'.format(api_key, UUID))
        response = response.json()
        if response['success'] is True:
            return response['session']
        else:
            raise HypixelAPIError(response)

class Guild:
    """ This class represents a guild on Hypixel as a single object.
        A guild has a name, members etc. """
    JSON = None
    GuildID = None
    def __init__(self, GuildID):
        if len(GuildID) == 24:
            self.GuildID = GuildID
            self.getJSON()

    def getJSON(self):
        """ This gets the guild's information from the Hypixel-API. """
        GuildID = self.GuildID
        api_key = choice(verified_api_keys) # Select a random API key from the list available.
        response = requests.get(HYPIXEL_API_URL + 'guild?key={}&id={}'.format(api_key, GuildID))
        response = response.json()
        if response['success'] is True:
            self.JSON = response['guild']
        else:
            raise HypixelAPIError(response)

    def getMembers(self):
        """ This function enumerates all the members in a guild.
            Mojang's API rate-limits this weirdly. You can use this as many times as you want,
            but it has to be a unique request. Duplicate requests of the same player are 1 min. """
        guildRoles = ['MEMBER', 'OFFICER', 'GUILDMASTER'] # Define variables etc.
        memberDict = self.JSON['members']
        allGuildMembers = {}
        for role in guildRoles: # Make allGuildMembers =
            allGuildMembers[role] = [] # {MEMBER: [], OFFICER: [], GUILDMASTER: []}

        for member in memberDict: # For each member, use Mojang's API to get their username.
            response = requests.get(MOJANG_SESSION_SERVER_URL + member['uuid'])
            response = response.json()
            for role in guildRoles: # Then sort them into the correct place in allGuildMembers.
                if member['rank'] == role:
                    allGuildMembers[role].append(response['name'])

        return allGuildMembers
