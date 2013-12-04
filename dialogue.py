from interpreter import BaseInterface
from cmd import Cmd


class Dialogue(object):

    def __init__(self):
        self.character = None
        self.dialogue = {}
        self.dialogue_name = None
        #dialogue choice that starts fight
        self.startsfight = ''
        self.givesitem = ''

class DialogueProcessor(object):
    
    def __init__(self, dialogue_name=None, world=None,game_engine=None):
        self.world = world
        self.game_engine = game_engine
        self.current_blurb = 'start'
        print('loading dialogue_name: %s' % dialogue_name)
        self.dialogue_name = self.world.dialogues.get(dialogue_name)
        self.currentChoiceMap = self.getChoiceMap()


    def startDialogue(self):
        returnStr = self.dialogue_name.dialogue.get('start') 
        returnStr += '\n\n' + self.displayChoices()
        return returnStr
    
    def displayChoices(self):
        returnStr = ''
        self.currentChoiceMap = self.getChoiceMap()
        for index, choice, desc in self.currentChoiceMap:
            returnStr += desc + '\n'
        return returnStr

    def getChoiceMap(self):
        index = 1
        choices = self.getChoices()
        self.currentChoiceMap = []
        for choice in choices:
            self.currentChoiceMap.append( [index,choice[1],str(index) + ') ' + choice[0]] )
            index = index + 1
        return self.currentChoiceMap
    
    def getChoices(self):
        return self.dialogue_name.dialogue.get(self.current_blurb + 'choices')
        
    def choice(self,c):
        for index, choice, desc in self.currentChoiceMap:
            if index == c:
                self.current_blurb = choice
                if self.dialogue_name.dialogue.get(self.current_blurb):
                    self.game_engine.cout(self.dialogue_name.dialogue.get(self.current_blurb))
                if self.dialogue_name.dialogue.get(self.current_blurb + 'choices'):
                    self.game_engine.cout(self.displayChoices())
                    break 
                else:
                    print('exiting....')
                    self.game_engine.do_exit(True)
                

class DialogueInterpreter(BaseInterface):
    
    dialogue_action = None
    
    def do_exit(self,s):
        self.game_out_q.put({'exit':True})

    def do_1(self,s):
        idx = 1
        self.game_out_q.put({'dialogue_choice':idx})

    def do_2(self,s):
        idx = 2
        self.game_out_q.put({'dialogue_choice':idx})
    
    def do_3(self,s):
        idx = 3
        self.game_out_q.put({'dialogue_choice':idx})
    
    def do_4(self,s):
        idx = 4
        self.game_out_q.put({'dialogue_choice':idx})
    
    def do_5(self,s):
        idx = 5
        self.game_out_q.put({'dialogue_choice':idx})
    
    def do_6(self,s):
        idx = 6
        self.game_out_q.put({'dialogue_choice':idx})
    
    def do_7(self,s):
        idx = 7
        self.game_out_q.put({'dialogue_choice':idx})
    
