import time
from cmd import Cmd
import threading
from queue import Queue
from load_world import LoadWorld,LoadCharacters
from dialogues import DialogueInterpreter
from character import Player,Weapon
from combat import FightInterpreter
from world_state import World
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug('Logging init...')


class Interface(Cmd,object):

	def __init__(self,world = None,queue=None):
		super(Interface,self).__init__(self)
		self.world = world
		self.world.current_state = self.world.LOADING
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
		self.queue = queue
		self.prompt = self.get_prompt()
		

	def postcmd(self,stop,line):
		self.prompt = self.get_prompt()
		
	
	def get_prompt(self):
		print('prompting')
		return \
		'**rpg**\nYou are in %s\nlook ->%s\nexits -> %s\n(>' % \
		(self.currentRoom,self.looktargets,self.exits)
	
	def do_exit(self,s):
		return True
	
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
			di.cmdloop()
			if(di.dialogue_action == True):
				pass
			else:
				if di.dialogue_action.get('action')=='Fight':
					log.debug('starting dialog fight %s' % self.characters[self.targets[s]])
					fi = FightInterpreter(player=self.player,character=self.characters[self.targets[s]])
					fi.cmdloop()


class GameEngine(threading.Thread):
	
	
	def __init__(self,world=None,queue=None):
		super(GameEngine,self).__init__(target=self)
		self.world = world
		self.request_queue = queue
		self.status = 'STARTING'
		
	
	def run(self):
		start_time = time.time()
		while True:
			elapsed = time.time() - start_time
			if elapsed % 10 == 0:
				print('%s Sec Elapsed' % elapsed )
				time.sleep(1)
	
	
	def cout(self,message):
		'''
		cout: prints output to player console
		'''
		print(message)



def main():
	print('what')
	w = World()
	q = Queue()
	i = Interface(world=w,queue=q)
# 	g = GameEngine(world=w,queue=q)
# 	g.start()
	i.cmdloop()
# 	g.join()

if __name__ == "__main__":
	main()
