### Version v0.6.0
Made all requests asynchronous! This has reduced the loading time of seven players, for example, from ~14s load time to ~5s load time.

### Version v0.5.0
This is a pretty polished version now. Just a few things to clean-up and a few improvements.

### Version v0.4.0
Create Travis Ci tests and simplified use of the library. 
#### Old:
variable = hypixel.Player('username').getJSON()
print(variable.getLevel())
print(variable.getJSON.JSON['networkExp'])
#### New:
variable = hypixel.Player('username')
print(variable.getLevel())
print(variable.JSON['networkExp'])