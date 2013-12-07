from cmd import Cmd
from random import randrange
from combat import FightInterpreter

class Character(object):
    """
    The base character class
    """

    character_id = None
    friendly_name = 'Shifty little man'
    inventory = []
    hp = 10
    armor_class = 1
    armor_type = 'cloth'
    active_weapon = None
    dead = False
    attack_on_sight = False
    isMovable = True

class Npc(Character):

    def __init__(self):
        pass
        
    def dialog(self):
        pass




class Monster(Character):

    def __init__(self,weapon=None):
        self.active_weapon = weapon

class Item(object):

    item_id = 'nullItem'
    friendly_name = 'Just an Item'
    

class Weapon(Item):

    item_id = 'nullWep'
    damage_type = 'blunt'
    friendly_name = 'little brown stick'
    attack = 4
    crit_chance = 3
    crit_multiplyer = 2
    defense = 0   


class Player(Character):

    def __init__(self,weapon=None):
        self.active_weapon = Weapon()

def main():
    w = Weapon()
    c = Monster(weapon=w)
    p = Player(weapon=w)
    p.armor_type = 'awesome'
    fi = FightInterpreter(character=c,player=p)
    fi.cmdloop()

if __name__ == "__main__":
    main()
