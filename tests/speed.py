""" Travis Ci Tests """

ActualData = ['8998bcff9765438bb6089ab93bfad4d3',
              'f7c77d999f154a66a87dc4a51ef30d19',
              'ed23c309c54645a7b4805f95a2fb76b0',
              '43db704e10b140b3a38dce059de35a59',
              '2b7f6bd60cfe4458a35a3312493772fb',
              '042470004a1f4f3bab91001866784bc0',
              'aec441cb6ee14601b000ec0ece396649',
              '0d062b017cc54b5da034fc17fc26206c',
              '446dea472dd0494b89260421b9981d15',
              'b80a30a6d6d7472490c0c6081684b769']

Repeats = 5

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import hypixel
from time import time
from random import shuffle

print("Test \"{}\" is now running...\n".format(os.path.basename(__file__)))

API_KEY = os.environ['apikey']

hypixel.setKeys([API_KEY])

start = time() # Start timer.

for i in range(0, Repeats-1):
    shuffle(ActualData) # Randomize the order of the data
    for InputUUID in ActualData:
        Player = hypixel.Player(InputUUID)
        print(Player.getPlayerInfo())

end = time()

totalTime = start-end

print("\nDone! Speed test finished. Time taken: {}".format(end-start))
