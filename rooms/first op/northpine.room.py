
from room import Room
r = Room()
r.roomname = 'northpine'
r.exits = {'intersection': 'intersection'}
r.roomdesc = """
north pine street houses number 36 and 42 are targets

"""
r.looktargets = {'house 36': 'its red\n\n',
                 'house 42': 'its blue\n\n'} 
