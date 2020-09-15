""" Travis Ci Tests """

ActualData = [
              {'Name': 'ByeByeBaePls',
              'Rank': {'wasStaff': False, 'rank': 'MVP+'},
              'Level': 13.7633,
              'GuildID': '54b9e7060cf2141da4fb3449',
              'Session': None},

              {'Name': 'kevinkool',
               'Rank': {'wasStaff': True, 'rank': 'MVP+'},
               'Level': 43.25043478260869,
               'GuildID': None,
               'Session': None},

              {'Name': 'canihasban',
               'Rank': {'wasStaff': False, 'rank': 'Non'},
               'Level': 1.053,
               'GuildID': None,
               'Session': None},

              {'Name': 'Kqwqii',
               'Rank': {'wasStaff': False, 'rank': 'MVP+'},
               'Level': 5.1,
               'GuildID': None,
               'Session': None}
              ]

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hypixel
import time

print(f"Test \"{os.path.basename(__file__)}\" is now running...\n")

API_KEY = os.environ['apikey']

hypixel.setKeys([API_KEY])

TestFailed = False

for player in ActualData:
    TestPlayer = hypixel.Player(player['Name'])
    for test in player:
        method_to_call = getattr(TestPlayer, 'get' + test)
        testdata = method_to_call()
        if testdata == player[test]:
            print(f"✔ {testdata}")
        else:
            print(f"❌ {testdata}, Expected: {player[test]} [FAILED]")
            TestFailed = True
    print(f"UUID: {TestPlayer.UUID}\n")

if TestFailed is True:
    raise ValueError


print("\nDone! All tests finished.")
