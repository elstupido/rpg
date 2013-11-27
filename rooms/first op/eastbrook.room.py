from room import Room
r = Room()
r.roomname = 'eastbrook'
r.exits = {'intersection': 'intersection'}
r.roomdesc = """
east brook street houses number 12 and 6 are targets

"""
r.looktargets = {'house 12': 'its red\n\n',
                 'house 6': 'its blue\n\n'} 
