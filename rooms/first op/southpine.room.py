from room import Room
r = Room()
r.roomname = 'southpine'
r.exits = {'intersection': 'intersection'}
r.roomdesc = """
south pine street houses number 22 and 16 are targets

"""
r.looktargets = {'house 22': 'its red\n\n',
                 'house 16': 'its blue\n\n'} 
