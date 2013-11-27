class Room(object):
    
    def __init__(self):
        self.roomname = None
        self.exits = None
        self.roomdesc = None
        self.looktargets = {}
        self.occupants = []
    
    