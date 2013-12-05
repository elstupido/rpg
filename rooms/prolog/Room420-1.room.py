
from room import Room
r = Room()
r.roomname = 'room 420'
r.exits = {'hallway': 'hallway'}
r.roomdesc = """
as the door opens smoke languidly rolls out. The lights are off and the curtain is pulled, which would normally make for a very dark room except for what appears to be a super nova sitting in the corner of the room. Anti political posters cover all the walls and some of the ceiling. a panel of six monitors sits on a desk, a few have news feeds and chat windows, the rest appear to be filled with code. the only other thing you can make out in the blinding light is the garret, sitting in his office chair, silhouetted like some kind of bizarre, techno angel.


"""
r.looktargets = {'blinding light': '(squinting)It apears to be some kind of computer, "whats that smell? burrned retninas you say"\n\n',
 'light': '(squinting)It apears to be some kind of computer, "whats that smell? burrned retninas you say"\n\n',
 'monitors': 'two of the monitors have news feeds detailing various horrors, one monitor has a few chat windows up where two people one named shifty and the other stupid seem to be conversing.\n\n',
 'posters': 'various posters striking out at governments and "the new world order." one poster which seems different from the rest. it has no words and no slogans on it just a black masked man watching as countless people walk down a road into a pitch black tunnel.\n\n'}
r.talktargets = {'garrett' : 'garret_1'}
r.characters = ['garret_1']