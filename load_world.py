from os import listdir,walk
from os.path import isfile,join
from character import Monster,Npc,Player,Weapon

roomdir = '.\\rooms\\'
dialoguedir = '.\\dialogues\\'
characterdir = '.\\characters\\'

class LoadCharacters(object):

    ALL_CHARACTERS = {}

    def __init__(self):
        character_name = None
        filelist = []
        character_dict ={}
        for root,directory,files in walk(characterdir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]
            
        for file in filelist:
            print('parsing %s' % file)
            fh = open(file)
            m = None
            execTarget = { 'm' : m }
            exec(fh.read(),execTarget)
            character_dict[execTarget['m'].character_id] = execTarget['m']

        self.ALL_CHARACTERS = character_dict
            


class LoadWorld(object):
    
    world = { 'Rooms' : {} }
    
    def __init__(self):
        roomName = None
        key = None
        roomDir = roomdir
        filelist = []
        for root,directory,files in walk(roomDir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]
        
        for file in filelist:
            print('parsing %s' % file)
            with open(file) as fh:
                for line in fh:
                    if line.find('$$$') == 0:
                        if line.split('$$$')[1].strip() == 'RoomName':
                            roomName = fh.readline()
                            roomName = roomName.strip().lower()
                            print('Found Room %s' % roomName)
                            self.world['Rooms'][roomName] = {}
                        else:
                            key = line.split('$$$')[1].strip().lower()
                    else:
                        if roomName and key:
                            if key == 'exits':
                                self.world['Rooms'][roomName][key] = line.strip().lower().split(',')
                            elif self.world['Rooms'][roomName].get(key):
                                self.world['Rooms'][roomName][key] += line
                            else:
                                self.world['Rooms'][roomName][key] = line


class LoadDialogues(object):
    
    world = { 'dialogue' : {} }
    
    def __init__(self):
        roomName = None
        key = None
        roomDir = dialoguedir
        filelist = []
        for root,directory,files in walk(roomDir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]

        for file in filelist:
            print('parsing %s' % file)
            with open(file) as fh:
                for line in fh:
                    if line.find('$$$') == 0:
                        if line.split('$$$')[1].strip() == 'character':
                            roomName = fh.readline()
                            roomName = roomName.strip().lower()
                            print('Found character dialog %s' % roomName)
                            self.world['dialogue'][roomName] = {}
                        else:
                            key = line.split('$$$')[1].strip().lower()
                    else:
                        if roomName and key:
                            if self.world['dialogue'][roomName].get(key):
                                self.world['dialogue'][roomName][key] += line
                            else:
                                self.world['dialogue'][roomName][key] = line
