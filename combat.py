from cmd import Cmd
from random import randrange
from interpreter import BaseInterpreter


class FightInterpreter(BaseInterpreter):

    def __init__(self,game_out_q=None, stdin=None, parent=None):
        super(FightInterpreter,self).__init__(self)
        self.game_out_q = game_out_q
        self.game_out_q.put({'cout':'^^^^^^STARTING COMBAT^^^^^^^^^^\n'})
        

    def do_attack(self,s):
        self.game_out_q.put({'player_attack':s})

    def do_run(self,s):
        self.game_out_q.put({'cout':'you run away, allowing %s to score a crit!' % (self.character.friendly_name) })
        self.game_out_q.put({'do_exit':s})



class Combat(object):

    def __init__(self,character=None,player=None,game_engine=None):
        self.character = character
        self.player = player
        self.game_engine = game_engine
        
    def roll_dice(self,numsides):
        return randrange(0,numsides+1)

    def attack(self,character):
        print(character)
        dice_sides = character.active_weapon.attack
        roll = self.roll_dice(dice_sides)
        return roll

    def defend(self,character):
        dice_sides = character.armor_class
        roll = self.roll_dice(dice_sides)
        return roll

    def player_attack(self,target):
        attack = self.process_attack(attacker=self.player,defender=self.character)
        self.game_engine.cout('======You Attack======\nYou attack with your %s\nYou roll %s, %s rolls %s.' % (self.player.active_weapon.friendly_name,
                                                                      attack['attack_roll'],
                                                                      self.character.friendly_name,
                                                                      attack['defend_roll'])) 
        if attack['blocked']:
            self.game_engine.cout('You are blocked by %s. No damage done.' % self.character.friendly_name )
        elif attack['stunned']:
            self.game_engine.cout('%s is stunned by your %s attack!' % (self.character.friendly_name,self.player.active_weapon.damage_type))  
        elif attack['fumble']:
            self.game_engine.cout('You fumble your attack and end up missing completely. No damage done.')
        else:
            if attack['crit']:
                self.game_engine.cout('CRITICAL HIT!')
            self.game_engine.cout('You hit for %s %s' % (self.character.friendly_name,attack['damage']) )
            self.apply_damage(character=self.character,damage=attack['damage'])
            
        self.game_engine.cout('(You %s: %s: %s) ' % (self.player.hp,self.character.friendly_name,self.character.hp))
        
        if self.character.dead:
            self.game_engine.cout('You kill %s\n======YOU WIN!=====\n' % self.character.friendly_name)
            return True
        else:
            defend = self.process_attack(attacker=self.character,defender=self.player)
            self.game_engine.cout('======%s Counter Attack======\n%s attacks with his %s\nYou roll %s, %s rolls %s.' % (self.character.friendly_name,
                                                                            self.character.friendly_name,
                                                                            self.character.active_weapon.friendly_name,
                                                                            defend['defend_roll'],
                                                                            self.character.friendly_name,
                                                                            defend['attack_roll']) )

            if defend['blocked']:
                self.game_engine.cout('You deftly block his attack. No damage done.')
            elif defend['fumble']:
                self.game_engine.cout('%s fumbles his attack, missing you completely. No damage done.' % self.character.friendly_name)
            else:
                if defend['crit']:
                    self.game_engine.cout('CRITICAL HIT!')
                self.game_engine.cout('%s hits You for %s' % (self.character.friendly_name,defend['damage']) )
                self.apply_damage(self.player,defend['damage'])
                self.game_engine.cout('(You %s: %s: %s) ' % (self.player.hp,self.character.friendly_name,self.character.hp))
                if self.player.dead:
                    self.game_engine.cout('======YOU ARE DEAD======\nThanks for playing asshole!')
                    return True
                return False
           

    def apply_damage(self,character=None,damage=0):
        character.hp = character.hp - damage
        if(character.hp < 1):
            character.dead = True
        

    def process_attack(self,attacker=None,defender=None,guarenteed_crit=False):
        attack_roll = self.attack(attacker)
        defend_roll = self.defend(defender)
        blocked = False
        fumble = False
        stunned = False
        crit_roll = 0
        crit = False
        damage = 0
        damage = attack_roll - defend_roll
        if attacker.active_weapon.damage_type == 'blunt':
            if defender.armor_type == 'cloth':
                if self.roll_dice(4) == 4:
                    stunned = True
        if defend_roll > attack_roll:
            blocked = True
        if damage == 0:
            fumble = True
        else:
            crit_roll = self.roll_dice(attacker.active_weapon.crit_chance)
            if attacker.active_weapon.crit_chance == crit_roll or guarenteed_crit:
                crit = True
                damage = damage * attacker.active_weapon.crit_multiplyer
        return { 'attack_roll' : attack_roll,
                 'defend_roll' : defend_roll,
                 'blocked'     : blocked,
                 'fumble'      : fumble,
                 'crit_roll'   : crit_roll,
                 'crit'        : crit,
                 'damage'      : damage,
                 'stunned'     : stunned,
                }

    
