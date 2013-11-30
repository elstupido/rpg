from os import listdir,walk
from os.path import isfile,join
from character import Monster,Npc,Player,Weapon
import pprint


class World(object):

    def __init__(self):
        self.roomdir = '.\\rooms\\'
        self.dialoguedir = '.\\dialogues\\'
        self.characterdir = '.\\characters\\'
        self.rooms = {}
        self.characters = {}
        self.players = {}
        self.dialogues = {}

    def loadCharacters(self):
        filelist = []
        character_dict ={}
        for root,empty,files in walk(self.characterdir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]
            
        for file in filelist:
            print('parsing %s' % file)
            fh = open(file)
            m = None
            exec_target = { 'm' : m }
            exec(fh.read(),exec_target)
            character_dict[exec_target['m'].character_id] = exec_target['m']

        self.characters = character_dict
                
    def loadRooms(self):
        filelist = []
        return_dict ={}
        for root,empty,files in walk(self.roomdir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f)) and f.find('.py') != -1]
            
        for file in filelist:
            print('parsing %s' % file)
            fh = open(file)
            exec_target = {}
            exec(fh.read(),exec_target)
            print(exec_target['r'])
            return_dict[exec_target['r'].roomname] = exec_target['r']

        self.rooms = return_dict

    def loadDialogues(self):
        filelist = []
        return_dict ={}
        for root,empty,files in walk(self.dialoguedir):
            filelist = filelist + [join(root,f) for f in files if isfile(join(root,f)) and f.find('.py') != -1]
            
        for file in filelist:
            print('parsing %s' % file)
            fh = open(file)
            exec_target = {}
            exec(fh.read(),exec_target)
            return_dict[exec_target['d'].dialogue_name] = exec_target['d']

        self.dialogues = return_dict

# "Depricated"
# class LoadWorld(object):
#     
#     world = { 'Rooms' : {} }
#     
#     def __init__(self):
#         roomName = None
#         key = None
#         roomDir = roomdir
#         filelist = []
#         for root,directory,files in walk(roomDir):
#             filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]
#         
#         for file in filelist:
#             if file.find('.py') == -1:
#                 print(file)
#                 roomName = None
#                 print('parsing %s' % file)
#                 with open(file) as fh:
#                     for line in fh:
#                         if line.find('$$$') == 0:
#                             if line.split('$$$')[1].strip() == 'RoomName':
#                                 roomName = fh.readline()
#                                 roomName = roomName.strip().lower()
#                                 print('Found Room %s' % roomName)
#                                 self.world['Rooms'][roomName] = {}
#                             else:
#                                 key = line.split('$$$')[1].strip().lower()
#                         else:
#                             if roomName and key:
#                                 if key == 'exits':
#                                     self.world['Rooms'][roomName][key] = line.strip().lower().split(',')
#                                 elif self.world['Rooms'][roomName].get(key):
#                                     self.world['Rooms'][roomName][key] += line
#                                 else:
#                                     self.world['Rooms'][roomName][key] = line
#                 with open(file + '.py','w') as out:
#                     exits = self.world['Rooms'][roomName].pop('exits',None)
#                     exits = dict([exit.split('=') for exit in exits])
#                     desc = self.world['Rooms'][roomName].pop('roomdesc')
#                     out.write("""
# from room import Room
# r = Room()
# r.roomname = '%s'
# r.exits = %s
# r.roomdesc = \"""
# %s
# \"""
# r.looktargets = %s
# """ %
# (roomName,pprint.pformat(exits),desc,pprint.pformat(self.world['Rooms'][roomName]))
# )


# class LoadDialogues(object):
#     
#     world = { 'dialogue' : {} }
#     
#     def __init__(self):
#         roomName = None
#         key = None
#         roomDir = '.\\dialogues\\'
#         filelist = []
#         for root,directory,files in walk(roomDir):
#             filelist = filelist + [join(root,f) for f in files if isfile(join(root,f))]
# 
#         for file in filelist:
#             print('parsing %s' % file)
#             with open(file) as fh:
#                 for line in fh:
#                     if line.find('$$$') == 0:
#                         if line.split('$$$')[1].strip() == 'character':
#                             roomName = fh.readline()
#                             roomName = roomName.strip().lower()
#                             print('Found character dialog %s' % roomName)
#                             self.world['dialogue'][roomName] = {}
#                         else:
#                             key = line.split('$$$')[1].strip().lower()
#                     else:
#                         if roomName and key:
#                             if self.world['dialogue'][roomName].get(key):
#                                 self.world['dialogue'][roomName][key] += line
#                             else:
#                                 self.world['dialogue'][roomName][key] = line
#             with open(file + '.py','w') as out:
#                 character = roomName
#                 dialogue = self.world['dialogue'][roomName]
#                 for key,value in dialogue.items():
#                     choice = []
#                     if key.find('choices') != -1:
#                         print(value)
#                         for v in value.split(','):
#                             choice.append(v.split('='))
#                         self.world['dialogue'][roomName][key] = choice
#                             
#                  
#                 out.write("""
# from dialogue import Dialogue
# self.character = %s
# self.dialogue = %s
# self.startsfight = ''
# self.givesitem = ''
# """ %
# (character,pprint.pformat(dialogue))
# )


def convertRoomFiles():
    import pprint
    w = World()
    w.loadRooms()
    w.loadCharacters()
    w.loadDialogues()
    print(w.rooms)
    print(w.characters)
    print(w.dialogues)

    
def main():
    convertRoomFiles()


if __name__ == "__main__":
    main()
