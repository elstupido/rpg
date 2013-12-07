from io import StringIO
import logging
from queue import Queue, Empty
import threading
import time
from tkinter import Tk, Frame, BOTH, Text, END, Entry, StringVar, font, RIGHT, \
	BOTTOM, LEFT, TOP

from character import Player, Weapon
from combat import FightInterpreter,Combat
from dialogue import DialogueInterpreter, DialogueProcessor
from interpreter import BaseInterpreter, TestInterpreter
from load_world import World
from ui import RPGText
from random import randrange


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#EVIL
log.debug = log.error
log.debug('Logging init...')

class RpgWindow(Frame):
	
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		#set up world and engine
		self.w = World()
		self.game_out_q = Queue()
		self.game_in_q = Queue()
		self.game_engine = GameEngine(world=self.w,queue=self.game_out_q,outqueue=self.game_in_q)
		self.game_engine.start()
		self.centerWindow()
		self.player_input = StringVar('')
		self.currentInterpreter = None
		self.baseInterpreter = None
		#fonts for highlighting targets
		self.output_stream_writer = None
		self.looktargets_font = font.Font(family="Helvetica",size=10,weight="bold")
		self.exits_font = font.Font(family="Helvetica",size=10,weight="bold",underline=True)
		#go go go
		self.initUI()
	
	def killBabies(self):
		print('killing babies')
		self.game_engine.exit = True
		self.currentInterpreter.exit = True
	
	def get_engine_output(self):
		messages = []
		go = False
		#check if we have new messages from game engine
		while not self.game_in_q.empty():
			messages.append(self.game_in_q.get())
			go = True
		#process messages if we have any
		if go:
			for message in messages:
				print(message)
				if 'display' == message[0]:
					self.output.insert(END,message[1])
					self.output.see(END)
					self.status_output.delete(1.0, END)
					self.status_output.insert(END, 'You are in %s' % self.game_engine.current_room.roomname)
					for target in self.game_engine.current_room.looktargets.keys():
						if target not in self.game_engine.current_room.hide_looktargets:
							self.output.highlight_pattern(target, 'looktargets')
					self.status_output.insert(END, '\n\nExits\n=========\n')
					for target in self.game_engine.current_room.exits.keys():
						if target not in self.game_engine.current_room.hide_exits:
							self.output.highlight_pattern(target, 'exits')
							self.status_output.insert(END,'%s\n' % target)
					if self.game_engine.current_room.characters:
						self.status_output.insert(END, '\n\nCharacters\n=========\n')
						for target in self.game_engine.current_room.characters:
							self.status_output.insert(END, target)
				if 'dialogue' == message[0]:
					self.currentInterpreter = self.currentInterpreter.start_dialogue(message[1])
					self.status_output.delete(1.0, END)
					self.status_output.insert(END, 'You are in %s' % self.game_engine.current_room.roomname)
					self.status_output.insert(END, '\nYou are talking to %s\n' % message[1])
				if 'combat' == message[0]:
					self.currentInterpreter = self.baseInterpreter
					self.currentInterpreter = self.currentInterpreter.start_combat(message[1])
					self.status_output.delete(1.0, END)
					self.output.insert(END,'\n=!=!=!=!=!=!=!=!=!=!=!=!=!=!=!=\nPrepare to Fight!\n\n\n')
					self.output.see(END)					
					self.status_output.insert(END, 'You are in %s' % self.game_engine.current_room.roomname)
					self.status_output.insert(END, '\nYou are Fighting %s\n' % message[1])
				if 'exit' == message[0]:
					self.currentInterpreter = self.baseInterpreter
					self.output.insert(END,'Exiting...\n\n')
					self.output.see(END)					

		#call ourself again
		self.after(1,self.get_engine_output)
	
	def get_player_input(self,player_input):
		#clear the entry object
		self.currentInterpreter.stdin = StringIO(self.player_input.get() + '\n')
		self.currentInterpreter.cmdloop(stop=False)
		self.player_console.delete(0, END)
		self.after_idle(self.get_engine_output)		
	
	def initUI(self):
		self.parent.title('RPG -- Really Pretty Good')
		#set up input/output console
		self.player_console = Entry(self.parent,textvariable=self.player_input)
		self.player_console.bind('<Return>', self.get_player_input)
		#set up output console
		self.output = RPGText(self.parent,wrap='word',height=29,width=80,bg='grey')
		self.status_output = RPGText(self.parent,wrap='word',height=4,width=20)
		self.output.tag_config('looktargets', font=self.looktargets_font)
		self.output.tag_config('exits', font=self.exits_font)
		
		#do whatever pack does
		#self.pack(fill = BOTH,expand = 1)
		self.status_output.pack(fill=BOTH,expand=1,side=RIGHT)
		self.output.pack(fill=BOTH,expand=1,side=TOP)
		self.player_console.pack(fill=BOTH,expand=1,side=BOTTOM)
		
		#set up interpreter
		self.baseInterpreter = Interface(world=self.w,game_out_q=self.game_out_q,parent=self.output)
		self.currentInterpreter = self.baseInterpreter 
		self.currentInterpreter.stdin = StringIO('look\n')
		self.currentInterpreter.cmdloop(stop=False)
		self.get_engine_output()
		
	def centerWindow(self):
		w = 720
		h = 488
		self.sw = self.parent.winfo_screenwidth()
		self.sh = self.parent.winfo_screenheight()
		x = (self.sw - w)/21
		y = (self.sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class Interface(BaseInterpreter):

	def start_dialogue(self,s):
		print('starting dialogue: %s' % s)
		i = DialogueInterpreter(stdin=self.stdin,game_out_q=self.game_out_q)
		i.prompt = self.prompt + ' > ' + s
		return i
	
	def start_combat(self,s):
		print('starting fight: %s' % s)
		i = FightInterpreter(stdin=self.stdin,game_out_q=self.game_out_q)
		return i
	
	def do_exit(self,s):
		return True
	
	def do_look(self,s):
		self.game_out_q.put({'do_look':s})		

	def do_go(self,s):
		self.game_out_q.put({'do_go':s})
		
	def do_talk(self,s):
		self.game_out_q.put({'do_talk' : s})
		
class GameEngine(threading.Thread):
	
	def __init__(self,world=None,queue=None,outqueue=None):
		super(GameEngine,self).__init__(target=self)
		self.world = world
		self.world.loadRooms()
		self.world.loadCharacters()
		self.world.loadDialogues()
		self.request_queue = queue
		self.out_queue = outqueue
		self.status = 'STARTING'
		self.current_room = self.world.rooms['testroom']
		self.DEBUG = True
		self.starting_wep = Weapon()
		self.player = Player(self.starting_wep)
		self.queue = queue
		self.exit = False
		#constructed at 'talk' time
		self.dialogue_processor = None
		self.combat_processor = None
		self.currentCharacterMap = {}
		self.current_state = ['loading']
	
	def run(self):
		last_move_time = time.mktime(time.localtime())
		move_timer = 90
		while True:
			time.sleep(0.09)
			curr_time = time.mktime(time.localtime())
			self.processMessages()
			if 'combat' not in self.current_state:
				if curr_time > last_move_time + move_timer:
					print('updating mobs') 
					self.updateMonsters()
					last_move_time = time.mktime(time.localtime())
			if self.exit:
				return True
	
	def updateCharacterMap(self):
		self.currentCharacterMap = {}
		for roomname, room in self.world.rooms.items():
			if room.characters:
				for character in room.characters:
					if self.world.characters.get(character).isMovable:
						self.currentCharacterMap[character] = room
	
			
	
	def updateMonsters(self):
		self.updateCharacterMap()
		for character, room in self.currentCharacterMap.items():
			if room.exits:
				for exit_name,exit in room.exits.items():
					print(exit)
					exit_room = self.world.rooms.get(exit)
					print(exit_room)
					if exit_room.mobsAllowed:
						room.characters.remove(character)
						exit_room.characters.append(character)
						if character in self.current_room.characters: 
							if self.world.characters.get(character).attack_on_sight:
								self.start_combat(character)
						break
					
						
					
						
		
	
	def processMessages(self):
		try:
			request = self.request_queue.get(block=False)
			for command,s in request.items():
				func = getattr(self, command)
				func(s)
				self.queue.task_done()
		except Empty:
			pass
	
	def do_exit(self,s):
		self.current_state = 'idle'
		self.out_queue.put(('exit',True))
	
	def do_look(self,s):
		log.debug(self.current_room.roomname)
		log.debug(self.current_room.looktargets)
		if(s):	
			thing = self.current_room.looktargets.get(s)
			if thing:
				self.cout(thing)
			else:
				self.cout("Try as you might, you can't see much more about %s\n\n" % s)
		else:
			self.cout(self.current_room.roomdesc)
		
	def do_go(self,s):
		exits = self.current_room.exits
		if s in exits.keys():
			self.current_room = self.world.rooms.get(exits[s])
			for character in self.current_room.characters:
				if self.world.characters.get(character).attack_on_sight:
					self.start_combat(character)
			self.do_look(None)
		
	def do_talk(self,s):
		if s in self.current_room.talktargets.keys():
			self.start_dialogue(self.current_room.talktargets.get(s))
	
	def prompt(self,s):
		self.out_queue.put(('prompt',self.current_room.roomname + '>'))
	
	def cout(self,message):
		'''
		cout: prints output to player console
		'''
		self.out_queue.put(('display' , message + '\n' ))
	
	def start_dialogue(self,s):
		'''
		start_dialogue: starts a dialogue
		'''
		#prepare processor
		self.current_state = ['dialogue']
		self.dialogue_processor = DialogueProcessor(world = self.world,dialogue_name = s,game_engine=self)
		self.dialogue_processor.startDialogue()
		self.out_queue.put(('dialogue',s)) 

	def dialogue_choice(self,s):
		self.dialogue_processor.choice(s)
		
	def start_combat(self,s):
		self.current_state = ['combat']
		self.combat_processor = Combat(player = self.world.player,character=self.world.characters.get(s),game_engine=self)
		self.out_queue.put(('combat',s))
	
	def player_attack(self,s):
		done = self.combat_processor.player_attack(s)
		if done:
			self.do_exit(True)

def main():
# 	w = World()
# 	q = Queue()
# 	iq = Queue()
# 	g = GameEngine(world=w,queue=q,outqueue=iq)
# 	i = Interface(world=w,queue=q,inqueue=iq)
# 	g.start()
# 	i.cmdloop('WELCOME TO RPG!!!\nPlease Enter Command\n')
	root = Tk()
	root.geometry('300x600+0+0')
	app = RpgWindow(root)
	root.mainloop()
	app.killBabies()

	
	
if __name__ == "__main__":
	main()
