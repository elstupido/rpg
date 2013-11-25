from character import Monster,Npc,Player,Weapon
m = Monster()
w = Weapon()
    
#set weapon attributes
w.weapon_id = 'mob_wep'
w.friendly_name = 'Mangey Paws'
w.attack = 2 
w.crit_chance = 100
w.crit_multiplyer = 2 
    
#set character attributes
m.character_id = 'test_monster'
m.friendly_name = 'MONSTER!'
m.hp = 10
m.armor_class = 5
m.defense = 0
m.attack  = 1
m.active_weapon = w
