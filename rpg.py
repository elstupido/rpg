import sys
import time
from cmd import Cmd
import threading
from queue import Queue,Empty
from load_world import World
from dialogues import DialogueInterpreter
from character import Player,Weapon
from combat import FightInterpreter
import logging
from tkinter import Tk, Frame, BOTH, Text, END, Entry, StringVar, font
import os
from ui import RPGText

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
		#pipe and string var for talking to console
		read,write = os.pipe()
		self.output_stream = os.fdopen(read,'r')
		self.output_stream_writer = os.fdopen(write,'w')
		self.player_input = StringVar('')
		#fonts for highlighting targets
		self.looktargets_font = font.Font(family="Helvetica",size=10,weight="bold")
		self.exits_font = font.Font(family="Helvetica",size=10,weight="bold",underline=True)
		#go go go
		self.initUI()
	
	def killBabies(self):
		print('killing babies')
		self.game_engine.exit = True
		self.interface.exit = True
	
	
	def get_engine_output(self):
		while not self.game_in_q.empty():
#			print(self.game_in_q.get())
			self.output.insert(END,self.game_in_q.get())
			self.output.see(END)
			for target in self.game_engine.current_room.looktargets.keys():
				if target not in self.game_engine.current_room.hide_looktargets:
					self.output.highlight_pattern(target, 'looktargets')
			for target in self.game_engine.current_room.exits.keys():
				if target not in self.game_engine.current_room.hide_exits:
					self.output.highlight_pattern(target, 'exits')
		self.after_idle(self.get_engine_output)
	
	def get_player_input(self,player_input):
		self.output_stream_writer.write(self.player_input.get() + '\n')
		self.output_stream_writer.flush()
		#clear the entry object
		self.player_console.delete(0, END)
		self.after_idle(self.get_engine_output)		
	
	def initUI(self):
		self.parent.title('RPG -- Really Pretty Good')
		self.pack(fill = BOTH,expand = 1)
		#set up input/output console
		self.player_console = Entry(self.parent,textvariable=self.player_input)
		self.output = RPGText(self.parent,wrap='word',height=29,width=30,bg='grey')
		self.output.tag_config('looktargets', font=self.looktargets_font)
		self.output.tag_config('exits', font=self.exits_font)
		
		self.player_console.bind('<Return>', self.get_player_input)
		self.output.pack(fill=BOTH)
		self.player_console.pack(fill=BOTH)
		
		#set up interpreter
		self.interface = Interface(world=self.w,game_out_q=self.game_out_q,stdin=self.output_stream,parent=self.output)
		self.interface.start()
		
	
		
	def centerWindow(self):
		w = 620
		h = 488
		self.sw = self.parent.winfo_screenwidth()
		self.sh = self.parent.winfo_screenheight()
		x = (self.sw - w)/21
		y = (self.sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class Interface(Cmd,threading.Thread):

	def __init__(self,world = None,game_out_q=None, stdin=sys.stdin, parent=None):
		Cmd.__init__(self)
		self.use_rawinput = False
		self.stdin = stdin
		threading.Thread.__init__(self)
		self.parent = parent
		self.game_out_q = game_out_q
		self.prompt = self.get_prompt()
		self.exit = False
		print('using input %s' % self.stdin)

	def run(self):
		self.cmdloop(self.intro)		
	
	def postcmd(self,stop,line):
		self.prompt = self.get_prompt()
		if self.exit:
			return True
	
	def get_prompt(self):
		return '(HAPPY THANKSGIVING! >' 
		#self.input.insert(END,'(>')
		#'**rpg**\nYou are in %s\nlook ->%s\nexits -> %s\n(>' % \
		#(self.current_room,self.looktargets,self.exits)
	
	def do_exit(self,s):
		return True
	
	def do_look(self,s):
		self.game_out_q.put({'do_look':s})		

	def do_go(self,s):
		self.game_out_q.put({'do_go':s})
		
	def do_talk(self,s):
		self.game_out_q.put({'do_talk':s})


class GameEngine(threading.Thread):
	
	
	def __init__(self,world=None,queue=None,outqueue=None):
		super(GameEngine,self).__init__(target=self)
		self.world = world
		self.world.loadRooms()
		self.world.loadCharacters()
		self.request_queue = queue
		self.out_queue = outqueue
		self.status = 'STARTING'
		self.current_room = self.world.rooms['dormroom']
		self.DEBUG = True
		self.starting_wep = Weapon()
		self.player = Player(self.starting_wep)
		self.queue = queue
		self.exit = False
	
	
	def run(self):
		start_time = time.time()
		while True:
			self.processUpdates()
			if self.exit:
				return True
	
	def processUpdates(self):
		try:
			time.sleep(0.09)
			request = self.request_queue.get(block=False)
			for command,s in request.items():
				func = getattr(self, command)
# 				self.cout('game thread processing command %s %s\n'%(command,s))
				func(s)
				self.queue.task_done()
		except Empty:
			pass

# 			except AttributeError:
# 				self.cout('cant find helper function for command %s' % command)
			
	
	
	def do_exit(self,s):
		return True
	
	def do_look(self,s):
		log.debug(self.current_room.roomname)
		log.debug(self.current_room.looktargets)
		if(s):	
			thing = self.current_room.looktargets.get(s)
			if thing:
				self.cout(thing)
			else:
				self.cout('Try as you might, you cant see much more about %s' % s)
		else:
			self.cout(self.current_room.roomdesc)
		
		

	def do_go(self,s):
		exits = self.current_room.exits
		if s in exits.keys():
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
		self.out_queue.put(message)




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
