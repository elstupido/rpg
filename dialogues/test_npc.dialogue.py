
from dialogue import Dialogue
d = Dialogue()
d.character = 'test_npc'
d.dialogue_name = 'test_npc'
d.dialogue = {'notsure': 'The old man laughs at you. He asks:\n    "Why would you say that?"\n\n',
 'notsurechoices': [['you look at your watch and say "no thanks I have to get going" you walk out into the hall',
                     'exit'],
                    ['\nlaughing you say "sure why not its not like I have a job interview any time soon." an hour or two later you lazily wonder out of garrets dorm room.',
                     'exit\n\n']],
 'start': 'The old man looks at you, but his eyes seem to be looking through you.\nAfter a unpleasantly long pause, he asks:\n    "Well young man, what do you say?"\n\n',
 'startchoices': [["um... I'm Not sure", 'notsure'],
                  ['\nWho are you?', 'who'],
                  ['\nScrew this old guy. I have things to do.', 'exit\n\n']],
 'who': 'The old man leans back a bit and his eyes sparkle with mirth.\nSuddenly, he moves with almost supernatural speed, getting right in your face.\n\n    "DO YOU KNOW WHO I AM?" He booms\n    "IM THE JUGGERNAUT..."\n    "BITCH."\n\n',
 }
d.startsfight = 'who'
d.givesitem = ''


