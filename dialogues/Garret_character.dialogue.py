
from dialogue import Dialogue
d = Dialogue()
d.character = 'garret_1'
d.dialogue_name = 'garret_1'
d.dialogue = {'camps': 'Garret glances over his shoulder at you, "you seem a bit stressed you should smoke a bowl.\n\n',
 'campschoices': [['you look at your watch and say "no thanks I have to get going" you walk out into the hall',
                   'exit'],
                  ['\nlaughing you say "sure why not its not like I have a job interview any time soon." an hour or two later you lazily wonder out of garrets dorm room.',
                   'exit \n\n']],
 'heya': '"A little bit of coding actually," Garret turns back and starts pondering one screen intently.\n\n',
 'heyachoices': [['You notice the poster that seems a bit out of place and ask "hey whats up with this poster garret"?',
                  'poster'],
                 ["\n'Oh what you working' on?", 'oh\n\n']],
 'interest': '"I will," he says excitedly "if you want you can help me with some of the rooms and dialog?!"\n\n',
 'interestchoices': [['"Uh no thanks I am really busy right now."', 'no'],
                     ['\n"sure why not could be fun."', 'sure\n\n']],
 'no': 'Garret shrugs resignedly, "ok ill send you a copy when its done."\n\n',
 'nochoices': [['lamely you change the subject. "Hey whats that odd poster over there?"',
                'poster\n\n\n\n\n\n\n\n\n\n\n\n']],
 'oh': '"I am creating a old school text based adventure game" he replies jovially. "I just finished creating a combat system and the "shifty little man" monster keeps kicking my ass he\'s just too shifty."\n\n',
 'ohchoices': [['with interest you peer over his shoulder at the screen but all you see is a open python shell and some initeligible text."Oh cool you will have to send it to me when you finish"',
                'interest\n\n']],
 'poster': 'Garret glaces at the poster you are pointing at, "that one? oh its about all the government abductions."\n\n',
 'posterchoices': [['"Uh....the what now?" you disbelievingly as you look at him out of the corner of your eye.',
                    'what\n\n']],
 'start': 'Garret swivels around in his chair, and and through a fit of suspect coughing, says,\n        "WORD...stack (character name), whats happenin."\n\n',
 'startchoices': [['heya Garret plotting the downfall of civilization again or programing',
                   'heya'],
                  ['\nyou start coughing uncontrollably and hurriedly back out of the room.',
                   'exit\n\n']],
 'sure': 'Garret bounces out of his chair and hands you a flopy "Great!! here is what I have so far.\'\n\n',
 'surechoices': [['As Garret hands you the flopy you notice  that odd poster again and ask him about it.',
                  'poster\n\n']],
 'what': 'Garret looks at you quizzically  "Ya, you know, all the people that get sent to the internment camps"\n\n',
 'whatchoices': [['"You mean the criminals and illegal aliens? they aren\'t abducted they are in those camps and for a good reason." you say a bit heatedly.',
                  'camps\n\n']]}
d.startsfight = ''
d.givesitem = ''
