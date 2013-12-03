from room import Room
r = Room()
r.roomname = 'dormroom'
r.exits = {'door': 'hallway', 'window': 'window'}
r.hide_exits = ['window']
r.hide_looktargets = ['under bed']
r.roomdesc = """
Your home away from home, its small but familiar. your unmade bed lies askew, one corner pulled slightly away from the wall. your hated alarm clock  and favorite book sit on your night stand by by the foot of your bed. across the room is your dresser containing your cloths and various knickknacks. the only other objects in the room are your trunk containing your school things which sits next to the door, and your computer which is resting on a flimsy desk, located by a very inviting window.


"""
r.looktargets = {'alarm clock': 'its black and noisy \n\n',
 'bed': 'your bed, cover by a black blanket with the white letters spelling  NAPPING ADVOCATE  #1\n\n',
 'behind bed': 'so thats where my pocket knife went! \n\n',
 'book': '1984 phew good thing this will never happen\n\n',
 'computer': 'good times, good times!!\n\n',
 'door': 'gate way to the outside world\n\n',
 'dresser': 'cloths in all the drawers but the top\n\n',
 'favorite book': '1984 phew good thing this will never happen\n\n',
 'night stand': 'a sturdy little table \n\n',
 'top drawer': 'Lock is stuck as usual if only I could find somthing to to jimmy  the lock.\n\n',
 'trunk': 'so many books!\n\n',
 'under bed': 'so thats where my pocket knife went! \n\n',
 'window': 'whata view! long way down though.\n\n',
 'door': 'the exit.\n\n',
 }
