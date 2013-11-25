from character import Monster,Npc,Player,Weapon
m = Monster()
w = Weapon()
    
#set weapon attributes
w.weapon_id = 'test_wep'
w.friendly_name = 'Old Man Stick Of Doom'
w.attack = 20 #up to 20 raw damage
w.crit_chance = 2 #50% chance to crit
w.crit_multiplyer = 4 #this stick HITS HARD
    
#set character attributes
m.character_id = 'test_npc'
m.friendly_name = 'Shifty old man'
m.hp = 100
m.armor_class = 5
m.defense = 0
m.attack  = 1
m.active_weapon = w


    

    
    
