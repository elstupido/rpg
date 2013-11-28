
from room import Room
r = Room()
r.roomname = 'intersection'
r.exits = {'north pine': 'northpine', 'south pine': 'southpine', 'east brook': 'eastbrook', 'west brook': 'westbrook', 'dorm street': 'dormstreet'}
r.roomdesc = """
where pine street and brook street intersect. pine street runs north southnbrook streed runs east west. starting place for op with erad.

"""
r.looktargets = {'erad': 'ROLL DOWN YOUR WINDOW!!!\n\n',}
