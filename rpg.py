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
from tkinter import Tk, Frame, BOTH, Text, END, Entry, StringVar
import os

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

#EVIL
log.debug = log.error
log.debug('Logging init...')

class RpgWindow(Frame):
	
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.w = World()
		self.q = Queue()
		self.iq = Queue()
		self.game_engine = GameEngine(world=self.w,queue=self.q,outqueue=self.iq)
		self.game_engine.start()
		self.centerWindow()
		read,write = os.pipe()
		self.output_stream = os.fdopen(read,'r')
		self.output_stream_writer = os.fdopen(write,'w')
		self.player_input = StringVar('')
		self.initUI()
	
	def killBabies(self):
		print('killing babies')
		self.game_engine.exit = True
		self.interface.stop = True
	
	def get_player_input(self,player_input):
		print(self.player_input.get())
		self.output_stream_writer.write(self.player_input.get() + '\n')
		self.output_stream_writer.flush()
		#clear the entry object
		self.player_console.delete(0, END)
	
	def initUI(self):
		self.parent.title('RPG -- Really Pretty Good')
		self.pack(fill = BOTH,expand = 1)
		#set up input/output console
		self.player_console = Entry(self.parent,textvariable=self.player_input)
		self.output = Text(self.parent,wrap='word',height=29,width=30,bg='grey')
		self.player_console.bind('<Return>', self.get_player_input)
		self.output.pack(fill=BOTH)
		self.player_console.pack(fill=BOTH)
		
		#set up interpreter
		self.interface = Interface(world=self.w,game_out_q=self.q,game_in_q=self.iq,stdin=self.output_stream,parent=self.output)
		self.interface.start()

	def centerWindow(self):
		w = 620
		h = 488
		self.sw = self.parent.winfo_screenwidth()
		self.sh = self.parent.winfo_screenheight()
		x = (self.sw - w)/2
		y = (self.sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class Interface(Cmd,threading.Thread):

	def __init__(self,world = None,game_out_q=None, game_in_q=None, stdin=sys.stdin, intro='HI!', parent=None):
		Cmd.__init__(self)
		self.use_rawinput = False
		self.stdin = stdin
		threading.Thread.__init__(self)
		self.parent = parent
		self.game_out_q = game_out_q
		self.game_in_q = game_in_q
		self.prompt = self.get_prompt()
		self.intro = intro
		self.exit = False
		print('using input %s' % self.stdin)

	def run(self):
		self.cmdloop(self.intro)		
	
	def postcmd(self,stop,line):
		self.prompt = self.get_prompt()
		if self.stop:
			return True
		time.sleep(0.1)
		while not self.game_in_q.empty():
#			print(self.game_in_q.get())
			self.parent.insert(END,self.game_in_q.get())
	
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
		self.current_room = self.world.rooms['intersection']
		self.DEBUG = True
		self.starting_wep = Weapon()
		self.player = Player(self.starting_wep)
		self.queue = queue
		self.exit = False
	
	
	def run(self):
		start_time = time.time()
		while True:
			time.sleep(0.01)
			self.processUpdates()
			if self.exit:
				return True
	
	def processUpdates(self):
		try:
			request = self.request_queue.get(block=False)
			self.cout(request)
			for command,s in request.items():
				func = getattr(self, command)
				self.cout('game thread processing command %s %s\n'%(command,s))
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
