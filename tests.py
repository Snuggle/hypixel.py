""" Travis Ci Tests """
import os
import hypixel

API_KEY = os.environ['apikey']

hypixel.setKeys([API_KEY])
Snuggle = hypixel.Player('8998bcff9765438bb6089ab93bfad4d3')

SnuggleLevel = Snuggle.getLevel()
if SnuggleLevel > 0:
    print("Snuggle's is level {}.".format(SnuggleLevel))
else:
    raise ValueError(SnuggleLevel)

SnuggleRank = Snuggle.getRank()
if SnuggleRank['rank'] == "Moderator":
    print("Snuggle's is a {}.".format(SnuggleRank))
else:
    raise ValueError(SnuggleRank)

SnuggleKarma = Snuggle.JSON['karma']
if SnuggleKarma > 0:
    print("Snuggle has {} karma.".format(SnuggleKarma))
else:
    raise ValueError(SnuggleKarma)

SnuggleGuildID = Snuggle.getGuildID()
SnuggleGuild = hypixel.Guild(SnuggleGuildID)
print("Snuggle's guild is called {}.".format(SnuggleGuild.JSON['name']))

print("\nDone! All tests finished successfully.")