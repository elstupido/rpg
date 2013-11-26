from cmd import Cmd
from load_world import LoadWorld,LoadDialogues,LoadCharacters
from dialogues import Dialogue,DialogueInterpreter
from character import Npc,Player,Monster,Weapon
from combat import FightInterpreter
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug('Logging init...')


class Interface(Cmd,object):

    def __init__(self):
        super(Interface,self).__init__(self)
        self.w = LoadWorld()
        self.currentRoom = 'testroom'
        self.room = self.w.world['Rooms'][self.currentRoom]
        self.DEBUG = True
        self.targets = None
        self.exits = None
        self.starting_wep = Weapon()
        self.player = Player(self.starting_wep)
        self.c = LoadCharacters()
        self.characters = self.c.ALL_CHARACTERS
        self.looktargets = []
        self.prompt = self.get_prompt()

    def postcmd(self,stop,line):
        self.prompt = self.get_prompt()
        

    def get_prompt(self):
        return \
        '**rpg**\nYou are in %s\nlook ->%s\nexits -> %s\n(Your Command, Sire?>' % \
        (self.currentRoom,self.looktargets,self.exits)
    
    def do_look(self,s):
        log.debug(self.currentRoom)
        self.room = self.w.world['Rooms'][self.currentRoom]
        self.looktargets = []
        for looktarget,description in self.room.items():
            if looktarget != 'exits' and looktarget != 'roomdesc' and looktarget != 'talktargets':
                self.looktargets.append(looktarget)
        if(s):    
            thing = self.room.get(s.lower())
            if thing:
                print(thing)
            else:
                print('Try as you might, you cant see much more about %s' % s)
        else:
            print(self.room.get('roomdesc'))
        

    def do_go(self,s):
        exitStr = self.room.get('exits')
        self.exits = {}
        for eachExit in exitStr:
            command,target = eachExit.split('=')
            self.exits[command] = target
        log.debug('exits: %s' % self.exits)
        if s in self.exits.keys():
            self.currentRoom = self.exits.get(s)
            self.do_look(None)

    def do_talk(self,s):
        raw_targets = self.room.get('talktargets')
        self.targets = {}
        if raw_targets:
            target_list = raw_targets.split(',')
            for target in target_list:
                key,value = target.split('=')
                self.targets[key]=value.rstrip()

        if s in self.targets.keys():
            di = DialogueInterpreter(dialogue=self.targets[s])
            resp = di.cmdloop()
            if(di.dialogue_action == True):
                pass
            else:
                if di.dialogue_action.get('action')=='Fight':
                    log.debug('starting dialog fight %s' % self.characters[self.targets[s]])
                    fi = FightInterpreter(player=self.player,character=self.characters[self.targets[s]])
                    fi.cmdloop()
                    
    

def main():
    i = Interface()
    i.cmdloop()

if __name__ == "__main__":
    main()
