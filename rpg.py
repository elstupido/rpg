from cmd import Cmd
from load_world import LoadWorld,LoadDialogues,LoadCharacters
from dialogues import Dialogue,DialogueInterpreter
from character import Npc,Player,Monster,Weapon
from combat import FightInterpreter
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
print(log.getEffectiveLevel())
log.debug('Logging init...')
log.info('WHAT THE FUCK IS THIS SHIT')

#HI SHIFTY!

class Interface(Cmd,object):


    
    w = LoadWorld()
    world = w
    currentRoom = 'testroom'
    room = w.world['Rooms'][currentRoom]
    DEBUG = True
    starting_wep = Weapon()
    player = Player(starting_wep)
    c = LoadCharacters()
    characters = c.ALL_CHARACTERS
    
    def do_look(self,s):
        log.debug(self.currentRoom)
        self.room = self.w.world['Rooms'][self.currentRoom]
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
        exits = {}
        for eachExit in exitStr:
            command,target = eachExit.split('=')
            exits[command] = target
        log.debug('exits: %s' % exits)
        if s in exits.keys():
            self.currentRoom = exits.get(s)
            self.do_look(None)

    def do_talk(self,s):
        raw_targets = self.room.get('talktargets')
        targets = {}
        if raw_targets:
            target_list = raw_targets.split(',')
            for target in target_list:
                key,value = target.split('=')
                targets[key]=value.rstrip()

        if s in targets.keys():
            di = DialogueInterpreter(dialogue=targets[s])
            resp = di.cmdloop()
            if(di.dialogue_action == True):
                pass
            else:
                if di.dialogue_action.get('action')=='Fight':
                    log.debug('starting dialog fight %s' % self.characters[targets[s]])
                    fi = FightInterpreter(player=self.player,character=self.characters[targets[s]])
                    fi.cmdloop()
                    
    

def main():
    i = Interface()
    i.cmdloop()

if __name__ == "__main__":
    main()
