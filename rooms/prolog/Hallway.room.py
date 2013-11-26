
from room import Room
r = Room()
r.roomname = 'hallway'
r.exits = {'dorm room': 'dormroom',
 'elevator': 'elevator',
 'room 420': 'room 420',
 'stairs': 'lounge'}
r.roomdesc = """
a somewhat dingy ill lit Hallway with many dorm rooms attached. You dont know any one on this floor except for that crazy anti government guy, Garret, who lives down the hall in room 420. the stairs are down the opposite end of the hall, while the sedate elevator is just a few doors down from your room.


"""
r.looktargets = {'420': 'is that smoke coming from under the door?!?!\n\n',
 'room 420': 'is that smoke coming from under the door?!?!\n\n'}
