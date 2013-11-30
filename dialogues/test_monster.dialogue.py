
from dialogue import Dialogue
d = Dialogue()
d.character = 'test_monster'
d.dialogue_name = 'test_monster'
d.dialogue = {
 'start': "You walk up to the monster and say 'hi'\nalmost as soon as the words leave your mouth\nhe leaps toward you!!\n\n",
 'startchoices': [['Continue...', 'exit\n\n']],
 }
d.startsfight = 'exit'
d.givesitem = ''


