class Room(object):
    
    def __init__(self):
        self.roomname = None
        self.exits = None
        self.roomdesc = None
        self.looktargets = {}
        self.characters = []
        self.players = []
        self.talktargets = []
        self.hide_exits = []
        self.hide_looktargets = []
        self.mobsAllowed = True

    
    