import time
from cmd import Cmd
import threading
from queue import Queue
from load_world import World
from dialogues import DialogueInterpreter
from character import Player,Weapon
from combat import FightInterpreter
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.debug('Logging init...')


class Interface(Cmd,object):

	def __init__(self,world = None,queue=None):
		super(Interface,self).__init__(self)
		self.queue = queue
		self.prompt = self.get_prompt()
		

	def postcmd(self,stop,line):
		self.prompt = self.get_prompt()
		
	
	def get_prompt(self):
		return '(broke the prompt, sorry>'
		#'**rpg**\nYou are in %s\nlook ->%s\nexits -> %s\n(>' % \
		#(self.current_room,self.looktargets,self.exits)
	
	def do_exit(self,s):
		return True
	
	def do_look(self,s):
		self.queue.put({'do_look':s})		

	def do_go(self,s):
		self.queue.put({'do_go':s})
		
	def do_talk(self,s):
		self.queue.put({'do_talk':s})


class GameEngine(threading.Thread):
	
	
	def __init__(self,world=None,queue=None):
		super(GameEngine,self).__init__(target=self)
		self.world = world
		self.world.loadRooms()
		self.world.loadCharacters()
		self.request_queue = queue
		self.status = 'STARTING'
		self.current_room = self.world.rooms['testroom']
		self.DEBUG = True
		self.starting_wep = Weapon()
		self.player = Player(self.starting_wep)
		self.queue = queue
	
	
	def run(self):
		start_time = time.time()
		while True:
			self.processUpdates()
	
	def processUpdates(self):
		request = self.request_queue.get()
		self.cout(request)
		for command,s in request.items():
			#get the function from locals() and run it
# 			try:
				func = getattr(self, command)
				print(s)
				func(s)
# 			except AttributeError:
# 				self.cout('cant find helper function for command %s' % command)
			
				
	def do_exit(self,s):
		return True
	
	def do_look(self,s):
		log.debug(self.current_room)
		self.looktargets = []
		for looktarget,description in self.current_room.looktargets.items():
			if looktarget != 'exits' and looktarget != 'roomdesc' and looktarget != 'talktargets':
				self.looktargets.append(looktarget)
		if(s):	
			thing = self.current_room.looktargets.get(s)
			if thing:
				print(thing)
			else:
				print('Try as you might, you cant see much more about %s' % s)
		else:
			print(self.current_room.roomdesc)
		

	def do_go(self,s):
		exits = self.current_room.exits
		if s in exits.keys():
			print(self.world.rooms)
			print(s)
			self.current_room = self.world.rooms.get(exits[s])
			self.do_look(None)

	def do_talk(self,s):
		targets = self.current_room.talktargets 
		if s in targets.keys():
			di = DialogueInterpreter(dialogue=targets[s])
			di.cmdloop()
			if(di.dialogue_action == True):
				pass
			else:
				if di.dialogue_action.get('action')=='Fight':
					log.debug('starting dialog fight %s' % self.characters[targets[s]])
					fi = FightInterpreter(player=self.player,character=self.characters[targets[s]])
					fi.cmdloop()
	
	def cout(self,message):
		'''
		cout: prints output to player console
		'''
		print('\n%s' % message)



def main():
	w = World()
	q = Queue()
	i = Interface(world=w,queue=q)
	g = GameEngine(world=w,queue=q)
	g.start()
	i.cmdloop()
	g.join()

if __name__ == "__main__":
	main()
