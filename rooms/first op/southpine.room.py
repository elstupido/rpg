from room import Room
r = Room()
r.roomname = 'southpine'
r.exits = {'intersection': 'intersection', 'house 16': 'house16', 'house 22': 'house22'}
r.roomdesc = """
south pine street houses number 22 and 16 are targets

"""
r.looktargets = {'house 22': 'its red\n\n',
                 'house 16': 'its blue\n\n'} 
