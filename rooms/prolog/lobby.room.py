
from room import Room
r = Room()
r.roomname = 'lobby'
r.exits = {'elevator': 'elevator', 'exit': 'exit', 'secutity room': 'securityroom', 'dorm street': 'dormstreet'}
r.roomdesc = """
a sparsely furnished lobby with a couple of chairs and a worn out couch. a trash can is laying on its side and garbage is strewn across the floor, a janitorial cart is already sitting by the mess but the janitor is noticeably absent. a building security officer is sleeping just outside his office.


"""
r.looktargets = {'chair': 'Hard plastic and sticky.\n\n',
 'couch': 'a very bitter looking couch\n\n',
 'trash': 'GAG! uuggh what in there.\n\n',
 'trash can': 'has a dent in the side, apears to have been kicked.\n\n'}
