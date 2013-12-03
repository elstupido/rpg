
from room import Room
r = Room()
r.roomname = 'lobby'
r.exits = {'elevator': 'elevator', 'exit': 'exit', 'security': 'secroom', 'dorm street': 'dormstreet'}
r.hide_looktargets = ['security center', 'security officer']
r.hide_exits = ['security center']
r.roomdesc = """
a sparsely furnished lobby with a couple of chairs and a worn out couch. a trash can is laying on its side and garbage is strewn across the floor, a janitorial cart is already sitting by the mess but the janitor is noticeably absent. a building security officer is sleeping just outside the building security center.


"""
r.looktargets = {'chair': 'Hard plastic and sticky.\n\n',
 'couch': 'a very dilapidated looking couch\n\n',
 'trash': 'GAG! uuggh whats in there.\n\n',
 'trash can': 'has a dent in the side, apears to have been kicked.\n\n',
 'security officer': 'sleeping on a stool next to the building security center.\n\n',
 'security center': 'a bullet proofed room with bars covering the large one way glass window overlooking the lobby.\n\n'
 } 
