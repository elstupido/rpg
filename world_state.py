class World(object):
    
    #world states
    LOADING = 0
    EXPLORING = 1
    DIALOG = 2
    FIGHT = 3
    
    
    def __init__(self):
        self.rooms = {}
        self.characters = {}
        self.items = {}    
        self.current_state = self.LOADING
        self.state = [self.current_state]
        self.current_interface = None