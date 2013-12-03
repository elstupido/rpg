
from room import Room
r = Room()
r.roomname = 'elevatorroof'
r.exits = {'elevator': 'elevator'}
r.roomdesc = """
Good God its dirty, some one left their tool box up here.


"""
r.looktargets = {'tool box': 'Tools for tooling\n\n',
                 'talktargets': 'figure=slm\n\n'}
