from cmd import Cmd
import sys

class BaseInterface(Cmd):

    def __init__(self,world = None,game_out_q=None, stdin=sys.stdin, parent=None):
        Cmd.__init__(self)
        self.use_rawinput = False
        self.parent = parent
        self.game_out_q = game_out_q
        self.exit = False
        print(str(__name__) + ' using input %s' % self.stdin)
    
    def cmdloop(self, intro=None,stop=True):
        """Repeatedly issue a prompt, accept input, parse an initial prefix
        off the received input, and dispatch to action methods, passing them
        the remainder of the line as argument.

        """

        self.preloop()
        if self.use_rawinput and self.completekey:
            try:
                import readline
                self.old_completer = readline.get_completer()
                readline.set_completer(self.complete)
                readline.parse_and_bind(self.completekey+": complete")
            except ImportError:
                pass
        try:
            if intro is not None:
                self.intro = intro
            if self.intro:
                self.stdout.write(str(self.intro)+"\n")
            stop = stop
            print(stop)
            while not stop:
                if self.cmdqueue:
                    line = self.cmdqueue.pop(0)
                else:
                    if self.use_rawinput:
                        try:
                            line = input(self.prompt)
                        except EOFError:
                            line = 'EOF'
                    else:
                        self.stdout.write(self.prompt)
                        self.stdout.flush()
                        line = self.stdin.readline()
                        print(line)
                        if not len(line):
                            line = 'EOF'
                        else:
                            line = line.rstrip('\r\n')
                line = self.precmd(line)
                stop = self.onecmd(line)
                stop = self.postcmd(stop, line)
                print(line)
                stop = True
            self.postloop()
        finally:
            stop = True
            if self.use_rawinput and self.completekey:
                try:
                    import readline
                    readline.set_completer(self.old_completer)
                except ImportError:
                    pass    
    
    def postcmd(self,stop,line):
        if self.exit:
            return True
        
class TestInterpreter(BaseInterface):
    
    def do_poop(self,s):
        print('got cmmand poop')
    
    def do_exit(self,s):
        self.game_out_q.put({'do_exit': None})
        
    def postcmd(self,stop,line):
        if self.exit:
            return True