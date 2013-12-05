
from room import Room
r = Room()
r.roomname = 'testroom2'
r.exits = {'up': 'testroom'}
r.roomdesc = """
As you look around, you notice there seems to be not much here.
it appears you can go up and get back to where you came from
there is a pile of gold and a large monster looking at you strangely.


"""
r.looktargets = {'gold': 'oooh. Shiny!\n\n',
 'monster': 'HOLY CRAP ITS A MONSTER\n\n',
 'pile': 'oooh. Shiny!\n\n',
 'pile of gold': 'oooh. Shiny!\n\n',
 }
r.talktargets = {'monster': 'test_monster'}
r.characters = ['test_monster']
