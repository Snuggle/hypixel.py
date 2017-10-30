""" Travis Ci Tests """

ActualData = [
              {'Name': 'ByeByeBaePls',
              'Rank': {'wasStaff': False, 'rank': 'MVP+'},
              'Level': 13.7633,
              'GuildID': '54b9e7060cf2141da4fb3449',
              'Session': None},

              {'Name': 'kevinkool',
               'Rank': {'wasStaff': True, 'rank': 'MVP+'},
               'Level': 43.20695652173913,
               'GuildID': None,
               'Session': None},

              {'Name': 'canihasban',
               'Rank': {'wasStaff': False, 'rank': 'Non'},
               'Level': 1.053,
               'GuildID': None,
               'Session': None},

              {'Name': 'Kqwqii',
               'Rank': {'wasStaff': False, 'rank': 'MVP+'},
               'Level': 2.4,
               'GuildID': None,
               'Session': None}
              ]

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hypixel
import time

print("Test \"{}\" is now running...\n".format(os.path.basename(__file__)))

API_KEY = os.environ['apikey']

hypixel.setKeys([API_KEY])

TestFailed = False

for player in ActualData:
    TestPlayer = hypixel.Player(player['Name'])
    for test in player:
        method_to_call = getattr(TestPlayer, 'get' + test)
        testdata = method_to_call()
        if testdata == player[test]:
            print("\U00002714 {}".format(testdata))
        else:
            print("\U0000274C {}, Expected: {} [FAILED]".format(testdata, player[test]))
            TestFailed = True
    print("UUID: {}\n".format(TestPlayer.UUID))

if TestFailed is True:
    raise ValueError


print("\nDone! All tests finished.")
