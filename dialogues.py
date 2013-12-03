from cmd import Cmd

class DialogueProcessor(object):
    
    def __init__(self, character, world):
        self.world = world
        self.current_blurb = 'start'
        self.character = self.d.world.dialogues.get(character)
        self.currentChoiceMap = self.getChoiceMap()


    def startDialogue(self):
        print(self.character.get('start'))
        f = self.displayChoices()
        if self.currentChoiceMap == []:
            if self.character.get(self.current_blurb + 'startsfight'):
                fight_target = self.character.get(self.current_blurb + 'startsfight')
                fight_target = fight_target.strip().lstrip().rstrip()
                if fight_target:
                    print('You prepare to fight!!')
                    return {'action':'Fight','target':fight_target}
            else:
                return False

    def displayChoices(self):
        self.currentChoiceMap = self.getChoiceMap()
        for index, choice, desc in self.currentChoiceMap:
            print( desc )

    def getChoiceMap(self):
        index = 1
        choices = self.getChoices()
        self.currentChoiceMap = []
        for targetChoice,description in choices.items():
            self.currentChoiceMap.append( [index,targetChoice,str(index) + ') ' + description] )
            index = index + 1
        return self.currentChoiceMap
    
    def getChoices(self):
        raw_choices = self.character.get(self.current_blurb + 'choices')
        choices = {}
        if raw_choices:
            for choice in raw_choices.split(','):
                value,key = choice.split('=') #swap key/value from file this makes same choice target impossible!
                choices[key.lstrip().rstrip()] = value.lstrip().rstrip()
        return choices
        
            

    def choice(self,c):
        for index, choice, desc in self.currentChoiceMap:
            if index == c:
                self.current_blurb = choice
                if self.character.get(self.current_blurb):
                    print(self.character.get(self.current_blurb))
                    if self.character.get(self.current_blurb + 'startsfight'):
                        fight_target = self.character.get(self.current_blurb + 'startsfight')
                        fight_target = fight_target.strip().lstrip().rstrip()
                        if fight_target:
                            print('You prepare to fight!!')
                            return {'action':'Fight','target':fight_target}
                if self.character.get(self.current_blurb + 'choices'):
                    self.displayChoices()
                    break
                elif self.character.get(self.current_blurb + 'startsfight'):
                    fight_target = self.character.get(self.current_blurb + 'startsfight')
                    fight_target = fight_target.strip().lstrip().rstrip()
                    if fight_target:
                        print('You prepare to fight!!')
                        return {'action':'Fight','target':fight_target} 
                else:
                    print('exiting....')
                    return True
                

class DialogueInterpreter(Cmd,object):
    
    dialogue_action = None
    
    def __init__(self, completekey='tab', stdin=None, stdout=None,dialogue=None, world = None):
        super(DialogueInterpreter,self).__init__(self)
        self.prompt = self.prompt + '(talk) '
        self.dialogue = DialogueProcessor(dialogue)
        self.dialogue_action = True
        response = self.dialogue.startDialogue()
        if response:
            self.dialogue_action = response

    def do_exit(self,s):
        return True
   
    def do_hi(self,s):
        print('HI YOUR DAMN SELF %s' % s)

    def do_1(self,s):
        idx = 1
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response

    def do_2(self,s):
        idx = 2
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response
    
    def do_3(self,s):
        idx = 3
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response
    
    def do_4(self,s):
        idx = 4
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response
    
    def do_5(self,s):
        idx = 5
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response
    
    def do_6(self,s):
        idx = 6
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response
    
    def do_7(self,s):
        idx = 7
        response = self.dialogue.choice(idx)
        self.dialogue_action = response
        return response

    
