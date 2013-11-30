
from dialogue import Dialogue
d = Dialogue()
d.character = 'g_man'
d.dialogue_name = 'g_man'
d.dialogue = {
 'start': 'you approach the official look in man sitting at the table covered in documentation and forms\n\n',
 'startchoices': [
                  ["""
                  you look at the documents on the table they appear to be for a government agency called 
                  NDEP national department of enforcement and protection you inquire as to its purpose'
                  """,'inquire'],
                  ['you glance at the table of documents along with the apparent G man scoff and walk away','exit'],
                 ],
 'inquire': 'Well "Iam glad you asked," the G man exclaimed with a ever broadening smile, "you see, we at the NDEP are ever vigilant in the defense of our great country!"',
 'inquirechoices': [
                    ['what exactly do you defend us from you say sarcastically...aliens?','threat'],
                   ],
 'threat': """
            Unphased,  the g man spreads his arms out, in a wide gesture, we protect and defend against any and every thing, 
            terrorists,spies, gangs. Basically any thing that proves it self a threat\n\n'
           """,
 'threatchoices': [
                   ['asking dubiously "aaaannddd...what exactly are you doing here"','recruit'],
                  ],
 'recruit': """
            Good question! I am here hoping to recruit some candidates to become NDEP operators. 
            Let me tell you its one hell of an opportunity. The pay is phenomenal and benefits are unsurpassed.
            The best part is you get government housing, transport and, gas vouchers!'
            """,
 'recruitchoices': [
                    ['trying to look nonchalant and failing rather spectacularly you ask the G man for his card and tell him you will think about his offer.','offer']
                   ],
 'offer': """
         He hands you his card and slaps you on the shoulder. 
         "Son you can contact me any time of day or night, and I'll  schedule an appointment down at the NDEP recruiting station.
        """,
 'offerchoices': [
                  ['you shake the G mans hand and walk way looking at his business card','exit']
                 ],
}
d.startsfight = ''
d.givesitem = ''
