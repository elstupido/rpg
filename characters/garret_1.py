from character import Monster,Npc,Player,Weapon
m = Monster()
w = Weapon()
    
#set weapon attributes
w.weapon_id = 'mob_wep'
w.friendly_name = 'Keyboard'
w.attack = 2 
w.crit_chance = 100
w.crit_multiplyer = 2 
    
#set character attributes
m.character_id = 'garret_1'
m.friendly_name = 'Garrett'
m.hp = 10
m.armor_class = 5
m.defense = 0
m.attack  = 1
m.attack_on_sight = False
m.active_weapon = w
