
from room import Room
r = Room()
r.roomname = 'testroom'
r.exits = {'under table': 'testroom2'}
r.roomdesc = """
This room seems very empty except for a small round table
in the very center. This table is covered by a white tablecloth
and has a single mysterious object sitting exactly in the center
of the table. Also there is an old man. 


"""
r.looktargets = {'object': 'You cant seem to descern what it is\n\n',
 'old man': 'He appears very old. maybe you should talk to him?\n\n',
 'table': 'This seems to be a normal table\n\n',
 'tablecloth': 'perfect white linen tablecloth. Nice!\n\n\n',
 'talktargets': 'old man=test_npc\n\n'}
