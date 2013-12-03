
from room import Room
r = Room()
r.roomname = 'elevator'
r.exits = {'ceiling': 'elevatorroof',
 'floor 1': 'lobby',
 'floor 2': 'lounge',
 'hallway': 'hallway'}
r.hide_looktargets = ['ceiling']
r.hide_exits = ['ceiling']
r.roomdesc = """
A very...very slow elevator with a very dirty carpet sained to the point of which its original color will forever remain a mystery and very sketchy light that flickers constantly and emits a buzzing sound. you notice a ceiling panel is out of place and hanging down a at one corner. there is a note next to the bottom two floors, floor 1 exit, floor 2 lounge 


"""
r.looktargets = {'carpet': 'I dont even want to think how it got that dirty\n\n',
 'ceiling': 'the emergency exit is out of place, wonder how that happened?\n\n',
 'light': 'DONT TOUCH THAT!\n\n'}
