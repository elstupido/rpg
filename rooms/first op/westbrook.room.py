from room import Room
r = Room()
r.roomname = 'westbrook'
r.exits = {'intersection': 'intersection', 'house 62': 'house62', 'house 56': 'house56'}
r.roomdesc = """
west brook street houses number 62 and 56 are targets

"""
r.looktargets = {'house 62': 'its red\n\n',
                 'house 56': 'its blue\n\n'} 
