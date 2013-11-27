
from room import Room
r = Room()
r.roomname = 'intersection'
r.exits = {'north pine': 'northpine', 'south pine': 'southpine', 'east brook': 'eastbrook', 'west brook': 'westbrook', 'dorm street': 'dormstreet'}
r.roomdesc = """
room where you start the op with erad.....

"""
r.looktargets = {'erad': 'ROLL DOWN YOUR WINDOW!!!\n\n',}
