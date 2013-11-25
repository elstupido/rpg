from cmd import Cmd
from random import randrange

class FightInterpreter(Cmd,object):

    def __init__(self, completekey='tab', stdin=None, stdout=None,character=None,player=None):
        import string, sys
        if stdin is not None:
            self.stdin = stdin
        else:
            self.stdin = sys.stdin
        if stdout is not None:
            self.stdout = stdout
        else:
            self.stdout = sys.stdout
        self.cmdqueue = []
        self.completekey = completekey
        self.preprompt = self.prompt
        self.prompt = self.preprompt + '(You %s: %s: %s) ' % (player.hp,character.friendly_name,character.hp)
        self.character = character
        self.player = player
        self.combat = Combat(character = self.character, player = self.player)
        print('^^^^^^STARTING COMBAT^^^^^^^^^^')
        

    def do_attack(self,s):
        end = self.combat.player_attack()
        self.updatePrompt()
        return end

    def do_run(self,s):
        print('you run away, allowing %s to score a crit!' % (self.character.friendly_name) )
        return True

    def updatePrompt(self):
        self.prompt = self.preprompt + '(You %s: %s: %s) ' % (self.player.hp,self.character.friendly_name,self.character.hp)


class Combat(object):

    def __init__(self,character=None,player=None):
        self.character = character
        self.player = player
        
    def roll_dice(self,numsides):
        return randrange(0,numsides+1)

    def attack(self,character):
        dice_sides = character.active_weapon.attack
        roll = self.roll_dice(dice_sides)
        return roll

    def defend(self,character):
        dice_sides = character.armor_class
        roll = self.roll_dice(dice_sides)
        return roll

    def player_attack(self):
        attack = self.process_attack(attacker=self.player,defender=self.character)
        print('======You Attack======\nYou attack with your %s\nYou roll %s, %s rolls %s.' % (self.player.active_weapon.friendly_name,
                                                                      attack['attack_roll'],
                                                                      self.character.friendly_name,
                                                                      attack['defend_roll'])) 
        if attack['blocked']:
            print('You are blocked by %s. No damage done.' % self.character.friendly_name )
        elif attack['stunned']:
            print('%s is stunned by your %s attack!' % (self.character.friendly_name,self.player.active_weapon.damage_type))  
        elif attack['fumble']:
            print('You fumble your attack and end up missing completely. No damage done.')
        else:
            if attack['crit']:
                print('CRITICAL HIT!')
            print('You hit for %s %s' % (self.character.friendly_name,attack['damage']) )
            self.apply_damage(character=self.character,damage=attack['damage'])
            
        if self.character.dead:
            print('You kill %s\n======YOU WIN!=====\n' % self.character.friendly_name)
            return True
        else:
            defend = self.process_attack(attacker=self.character,defender=self.player)
            print('======%s Counter Attack======\n%s attacks with his %s\nYou roll %s, %s rolls %s.' % (self.character.friendly_name,
                                                                            self.character.friendly_name,
                                                                            self.character.active_weapon.friendly_name,
                                                                            defend['defend_roll'],
                                                                            self.character.friendly_name,
                                                                            defend['attack_roll']) )

            if defend['blocked']:
                print('You deftly block his attack. No damage done.')
            elif defend['fumble']:
                print('%s fumbles his attack, missing you completely. No damage done.' % self.character.friendly_name)
            else:
                if defend['crit']:
                    print('CRITICAL HIT!')
                print('%s hits You for %s' % (self.character.friendly_name,defend['damage']) )
                self.apply_damage(self.player,defend['damage'])
                if self.player.dead:
                    print('======YOU ARE DEAD======\nThanks for playing asshole!')
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

    
