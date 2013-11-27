import time
from cmd import Cmd
import threading
from queue import Queue,Empty
from load_world import World
from dialogues import DialogueInterpreter
from character import Player,Weapon
from combat import FightInterpreter
import logging
from tkinter import Tk, Frame, BOTH, Text, END, Entry


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
#EVIL
#log.debug = log.error
log.debug('Logging init...')

class RpgWindow(Frame):
	
	def __init__(self,parent):
		Frame.__init__(self,parent)
		self.parent = parent
		self.w = World()
		self.q = Queue()
		self.iq = Queue()
		self.g = GameEngine(world=self.w,queue=self.q,outqueue=self.iq)
		self.g.start()
		self.initUI()
		self.centerWindow()
		
	def initUI(self):
		self.parent.title('RPG -- Really Pretty Good')
		self.pack(fill = BOTH,expand = 1)
		self.player_console = Entry(self.parent)
		self.output = Text(self.parent,height=30.0,width=30,bg='red')
		self.output.pack(fill=BOTH)
		self.player_console.pack(fill=BOTH)
		self.i = Interface(world=self.w,queue=self.q,inqueue=self.iq,output = self.output,input=self.player_console)
		self.i.start()

	def centerWindow(self):
		w = 620
		h = 480
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


class Interface(Cmd,threading.Thread):

	def __init__(self,world = None,queue=None, inqueue=None, input=None, output=None):
		Cmd.__init__(self)
		threading.Thread.__init__(self)
		self.queue = queue
		self.in_queue = inqueue
		self.output = output
		self.input = input
		self.prompt = self.get_prompt()
		
# 	def precmd(self,stop,line):
# 		line = self.input.get()
# 		print('got command %s' % line)
	
	def postcmd(self,stop,line):
		self.prompt = self.get_prompt()
		time.sleep(0.1)
		while not self.in_queue.empty():
			print(self.in_queue.get())
# 			self.parent.insert(END,self.in_queue.get())
	
	def get_prompt(self):
		return '(broke the prompt, sorry >' 
		#self.input.insert(END,'(>')
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
	
	
	def __init__(self,world=None,queue=None,outqueue=None):
		super(GameEngine,self).__init__(target=self)
		self.world = world
		self.world.loadRooms()
		self.world.loadCharacters()
		self.request_queue = queue
		self.out_queue = outqueue
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
		try:
			request = self.request_queue.get(block=False)
			self.cout(request)
			for command,s in request.items():
				func = getattr(self, command)
				self.cout('game thread processing command %s %s'%(command,s))
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
	w = World()
	q = Queue()
	iq = Queue()
	g = GameEngine(world=w,queue=q,outqueue=iq)
	i = Interface(world=w,queue=q,inqueue=iq)
	g.start()
	i.cmdloop('WELCOME TO RPG!!!\nPlease Enter Command\n')
# 	root = Tk()
# 	root.geometry('300x600+0+0')
# 	app = RpgWindow(root)
# 	root.mainloop()
	 
if __name__ == "__main__":
	main()
