""" Simple Hypixel-API in Python, by Snuggle | 2017-09-30 to 2018-06-14 """
__version__ = '0.8.0'
# pylint: disable=C0103
# TODO: Add more comments. Explain what's happening!
# TODO: Add API-usage stat-tracking. Like a counter of the number of requests and how many per minute etc.

from random import choice
from time import time, sleep
from datetime import datetime, timedelta
from copy import deepcopy
from typing import List, Iterable, Dict, Union, Optional
import grequests

import leveling

HYPIXEL_API_URL = 'https://api.hypixel.net/'
UUIDResolverAPI = "https://sessionserver.mojang.com/session/minecraft/profile/"

HYPIXEL_API_KEY_LENGTH = 36 # This is the length of a Hypixel-API key. Don't change from 36.
verified_api_keys: List[str] = []

requestCache: Dict[str, Dict] = {}
cacheTime = 60

class PlayerNotFoundException(Exception):
    """ Simple exception if a player/UUID is not found. This exception can usually be ignored.
        You can catch this exception with ``except hypixel.PlayerNotFoundException:`` """
    pass
class SkyblockUUIDRequired(Exception):
    """Simple exception to tell the user that in the Skyblock API, UUID's are required and names cannot be used.
    Catch this exception with ``except hypixel.SkyblockUUIDRequired:``"""
    pass
class GuildIDNotValid(Exception):
    """ Simple exception if a Guild is not found using a GuildID. This exception can usually be ignored.
        You can catch this exception with ``except hypixel.GuildIDNotValid:`` """
    pass

class HypixelAPIError(Exception):
    """ Simple exception if something's gone very wrong and the program can't continue. """
    pass

sleep_till: Optional[datetime] = None
def getJSON(typeOfRequest: str, **kwargs) -> dict:
    """ This private function is used for getting JSON from Hypixel's Public API. """
    global sleep_till

    if sleep_till and (sleep_duration := (sleep_till - datetime.now()).total_seconds()) >= 0:
        sleep(sleep_duration)
    sleep_till = None

    requestEnd = ''
    api_key = choice(verified_api_keys) # Select a random API key from the list available.

    if typeOfRequest == 'player':
        UUIDType = 'uuid'
        uuid = kwargs['uuid']
        if len(uuid) <= 16:
            UUIDType = 'name' # TODO: I could probably clean this up somehow.
    if typeOfRequest == 'skyblockplayer':
        typeOfRequest = "/skyblock/profiles"
    for name, value in kwargs.items():
        if typeOfRequest == "player" and name == "uuid":
            name = UUIDType
        requestEnd += f"{'&' if requestEnd else ''}{name}={value}"

    cacheURL = f"{HYPIXEL_API_URL}{typeOfRequest}?{requestEnd}"
    # TODO: Maybe lowercase for cache. However, certain query param names are for some reason
    # actually case sensitive, such as `byUuid` and `byName` (not sure if it's limited to these two).
    allURLS = [cacheURL]

    # If url exists in request cache, and time hasn't expired...
    if cacheURL in requestCache and requestCache[cacheURL]['cacheTime'] > time():
        response = deepcopy(requestCache[cacheURL]['data']) # TODO: Extend cache time
    else:
        requests = (grequests.get(u, headers={"API-Key": api_key}) for u in allURLS)
        responses = grequests.imap(requests)
        for r in responses:
            fullResponse = r
        response, responseHeaders = fullResponse.json(), fullResponse.headers

        if 'RateLimit-Remaining' in responseHeaders and int(responseHeaders['RateLimit-Remaining']) <= 1:
            sleep_till = datetime.now() + timedelta(seconds=int(responseHeaders['RateLimit-Reset'])+1)

        if not response['success']:
            raise HypixelAPIError(response)
        if typeOfRequest == 'player':
            if response['player'] is None:
                raise PlayerNotFoundException(uuid)
        if typeOfRequest != 'key': # Don't cache key requests.
            requestCache[cacheURL] = {}
            requestCache[cacheURL]['data'] = response
            requestCache[cacheURL]['cacheTime'] = time() + cacheTime # Cache request and clean current cache.
            cleanCache()
    try:
        return response[typeOfRequest]
    except KeyError:
        return response

def cleanCache():
    """ This function is occasionally called to clean the cache of any expired objects. """
    itemsToRemove = []
    for item in requestCache:
        try:
            if requestCache[item]['cacheTime'] < time():
                itemsToRemove.append(item)
        except:
            pass
    for item in itemsToRemove:
        requestCache.pop(item)


def setCacheTime(seconds):
    """ This function sets how long the request cache should last, in seconds.

        Parameters
        -----------
        seconds : float
            How long you would like Hypixel-API requests to be cached for.
    """
    try:
        global cacheTime
        cacheTime = float(seconds)
        return "Cache time has been successfully set to {} seconds.".format(cacheTime)
    except ValueError as chainedException:
        raise HypixelAPIError("Invalid cache time \"{}\"".format(seconds)) from chainedException

def setKeys(api_keys: list):
    """ This function is used to set your Hypixel API keys.

        Parameters
        -----------
        api_keys : list
            A list of the API keys that you would like to use.

            Example: ``['740b8cf8-8aba-f2ed-f7b10119d28']``.
    """
    for api_key in api_keys:
        if len(api_key) == HYPIXEL_API_KEY_LENGTH:
            verified_api_keys.append(api_key)
        else:
            raise HypixelAPIError("hypixel/setKeys: The key '{}' is not 36 characters.".format(api_key))

class Player:
    """ This class represents a player on Hypixel as a single object.
        A player has a UUID, a username, statistics etc.

        Raises
        ------
        PlayerNotFoundException
            If the player cannot be found, this will be raised.

        Parameters
        -----------
        Username/UUID : string
            Either the UUID or the username (Deprecated) for a Minecraft player.

        Attributes
        -----------
        JSON : string
            The raw JSON receieved from the Hypixel API.

        UUID : string
            The player's UUID.
    """

    def __init__(self, UUID: str):
        """ This is called whenever someone uses, e.g., hypixel.Player('Snuggle').
            Creates an object representing calls to the Hypixel API and info for this player. """
        if len(UUID) > 16 and len(UUID) not in (32, 36):
            raise PlayerNotFoundException(UUID)
        self.JSON = getJSON('player', uuid=UUID) # Get the player's Hypixel-API JSON information.
                                                 # Even if `UUID` is actually the ign, this still works.
        self.UUID: str = self.JSON['uuid']

    def getPlayerInfo(self) -> dict:
        """ This is a simple function to return a bunch of common data about a player. """
        JSON = self.JSON
        playerInfo = {'uuid': self.UUID, 'displayName': self.getName(),
                      'rank': self.getRank(), 'networkLevel': self.getLevel()}
        JSONKeys = ['karma', 'firstLogin', 'lastLogin',
                    'mcVersionRp', 'networkExp', 'socialMedia', 'prefix']
        for item in JSONKeys:
            try:
                playerInfo[item] = JSON[item]
            except KeyError:
                pass
        return deepcopy(playerInfo)

    def getName(self) -> str:
        """ Just return player's name. """
        JSON = self.JSON
        return JSON['displayname']

    def getLevel(self):
        """ This function calls leveling.py to calculate a player's network level. """
        JSON = self.JSON

        networkExp = JSON.get('networkExp', 0)
        networkLevel = JSON.get('networkLevel', 0)

        exp = leveling.getExperience(networkExp, networkLevel)
        myoutput = leveling.getExactLevel(exp)
        return myoutput

    def getUUID(self) -> str:
        """ This function returns a player's UUID. """
        JSON = self.JSON
        return JSON['uuid']

    def getRank(self) -> dict:
        """ This function returns a player's rank, from their data. """
        JSON = self.JSON
        playerRank: Dict[str, Union[bool, str]] = {} # Creating dictionary.
        playerRank['wasStaff'] = False
        possibleRankLocations = ['packageRank', 'newPackageRank', 'monthlyPackageRank', 'rank']
        # May need to add support for multiple monthlyPackageRank's in future.

        for Location in possibleRankLocations:
            if Location in JSON:
                if Location == 'rank' and JSON[Location] == 'NORMAL':
                    playerRank['wasStaff'] = True
                else:
                    if JSON[Location] == "NONE": # If monthlyPackageRank expired, ignore "NONE". See: https://github.com/Snuggle/hypixel.py/issues/9
                        continue
                    dirtyRank = JSON[Location].upper().replace("_", " ").replace(" Plus", "+")
                    playerRank['rank'] = dirtyRank.replace("Superstar", "MVP++").replace("Youtuber", "YouTube")

        if 'rank' not in playerRank:
            playerRank['rank'] = 'Non'

        return playerRank

    def getGuildID(self) -> str:
        """ This function is used to get a GuildID from a player. """
        UUID = self.UUID
        GuildID = getJSON('findGuild', byUuid=UUID)
        return GuildID['guild']

    def getSession(self):
        """ This function is used to get a player's session information. """
        UUID = self.UUID
        try:
            session = getJSON('session', uuid=UUID)
        except HypixelAPIError:
            session = None
        return session

    def isOnline(self) -> bool:
        """ This function returns a bool representing whether the player is online. """
        return getJSON('status', uuid=self.UUID)['session']['online']

    def getPitXP(self) -> int:
        return self._nestedGet(('stats', 'Pit', 'profile', 'xp'), 0)

    def getBedwarsXP(self) -> int:
        xp = self._nestedGet(('stats', 'Bedwars', 'Experience'), 0)
        assert int(xp) == xp # If xp is a float type, ensure its decimal part is just 0.
        return int(xp)

    def getBedwarsStar(self) -> int:
        return self._nestedGet(('achievements', 'bedwars_level'), 0)

    def getBedwarsFinalKills(self) -> int:
        return self._nestedGet(('stats', 'Bedwars', 'final_kills_bedwars'), 0)

    def getBedwarsFinalDeaths(self) -> int:
        return self._nestedGet(('stats', 'Bedwars', 'final_deaths_bedwars'), 0)

    def _nestedGet(self, nested_keys: Iterable, default_val):
        d = self.JSON
        try:
            for k in nested_keys:
                d = d[k]
            return_val = d
        except KeyError:
            return_val = default_val
        if not isinstance(return_val, (str, float, int)):
            return_val = deepcopy(return_val) # may be a mutable type
        return return_val

class Guild:
    """ This class represents a guild on Hypixel as a single object.
        A guild has a name, members etc.

        Parameters
        -----------
        GuildID : string
            The ID for a Guild. This can be found by using `player.getGuildID()`,
            where `player` is an object of the `Player` class.


        Attributes
        -----------
        JSON : string
            The raw JSON receieved from the Hypixel API.

        GuildID : string
            The Guild's GuildID.
    """

    def __init__(self, GuildID: str):
        try:
            if len(GuildID) == 24:
                self.GuildID = GuildID
                self.JSON = getJSON('guild', id=GuildID)
        except Exception as chainedException:
            raise GuildIDNotValid(GuildID) from chainedException

    def getMembers(self):
        """ This function enumerates all the members in a guild.
        Mojang's API rate-limits this weirdly.
        This is an extremely messy helper function. Use at your own risk. """
        guildRoles = ['MEMBER', 'OFFICER', 'GUILDMASTER'] # Define variables etc.
        memberDict = self.JSON['members']
        allGuildMembers = {}
        for role in guildRoles: # Make allGuildMembers =
            allGuildMembers[role] = [] # {MEMBER: [], OFFICER: [], GUILDMASTER: []}
        allURLS = []
        URLStoRequest = []
        roleOrder = []
        memberList = []
        requests = None
        responses = None
        for member in memberDict: # For each member, use the API to get their username.
            roleOrder.append(member['rank'])
            if UUIDResolverAPI + member['uuid'] in requestCache:
                print("cached")
                allURLS.append(requestCache[UUIDResolverAPI + member['uuid']]['name'])
            else:
                print("NOPE")
                allURLS.append(UUIDResolverAPI + member['uuid'])
                URLStoRequest.append(UUIDResolverAPI + member['uuid'])
        requests = (grequests.get(u) for u in URLStoRequest)
        responses = grequests.map(requests)
        for response in responses:
            requestCache[UUIDResolverAPI + response.json()['id']] = response.json()
        i = 0
        for uindex, user in enumerate(allURLS):
            try:
                if user.startswith(UUIDResolverAPI):
                    allURLS[uindex] = responses[i].json()['name']
                    i += 1
            except AttributeError:
                pass
        i = 0
        for name in allURLS:
            try:
                member = {'role': roleOrder[i], 'name': name}
            except KeyError:
                member = {'role': roleOrder[i], 'name': 'Unknown'}
            memberList.append(member)
            i = i + 1
        for member in memberList:
            roleList = allGuildMembers[member['role']]
            roleList.append(member['name'])

        return allGuildMembers


class Auction:
    """ This class represents an auction on Hypixel Skyblock as a single object. """
    def __init__(self):
        """"Called to create an Auction class."""
        pass
    def getAuctionInfo(self, PageNumber):
        """Gets all the auction info for a specified page. PageNumber is the page that is requested and can be in int form or string"""
        return getJSON("skyblock/auction", page = str(PageNumber))
    #TODO Add more info

class SkyblockPlayer:
    """A class for a Skyblock player. It requires a UUID, and will return stats on the player
    Raises
    ------
    SkyblockUUIDRequired
        If you pass in a normal username such as RedKaneChironic, will throw an error as Hypixel Skyblock's API currently does not support usernames
    PlayerNotFoundException
        If the player cannot be found, this will be raised.

    Parameters
    -----------
    UUID: string
        UUID of the Player
    JSON: string
        Raw JSON data"""
    def __init__(self, UUID):
        self.UUID = UUID
        if len(UUID) <= 16: #UUID is a Minecraft username
            raise SkyblockUUIDRequired(UUID)
        elif len(UUID) in (32, 36):
            self.JSON = getJSON('skyblock/player', uuid = UUID)
        else:
            raise PlayerNotFoundException(UUID)

if __name__ == "__main__":
    print("This is a Python library and shouldn't be run directly.\n"
          "Please look at https://github.com/Snuggle/hypixel.py for usage & installation information.")
