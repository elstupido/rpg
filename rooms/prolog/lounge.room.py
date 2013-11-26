
from room import Room
r = Room()
r.roomname = 'lounge'
r.exits = {'elevator': 'elevator', 'stairs': 'hallway'}
r.roomdesc = """
medium sized room with tiled floors and drop ceilings filled with an assortment of chairs couches and tables. a few people sit in groups here and there. A bulletin board stands off in the corner and a rather official looking man sits at a table piled high with pamphlets


"""
r.looktargets = {'bulletin board': 'various posters and pamphlets.\n\n',
 'chairs': 'scattered around the room as groups needed\n\n',
 'couches': 'mostly vacant, with and ocasional napper.\n\n',
 'man': 'looks to be recruiting for somthing. He Motions for you to come over and talk.\n\n',
 'offical man': 'looks to be recruiting for somthing. He Motions for you to come over and talk.\n\n',
 'people': 'groups here and there, either studying or finding various ways to pass the time.\n\n',
 'talktargets': 'man=g_man\n\n'}
