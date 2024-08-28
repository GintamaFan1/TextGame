extends Enemy1
class_name Ranger

var attack_damage:float = 10
var knock_back:float  = 100
var stun_time: float = .7

func attack(player):
	var attack = Attack.new()
	
	attack.attack_damage = attack_damage
	attack.knock_back = knock_back
	attack.stun_time = stun_time
	attack.attacker = self
	attack.attacked_enemy = player

	if player.name == "Character":
		if player.has_node("HitboxComponent"):
			var hitbox = player.get_node("HitboxComponent")
			if hitbox:
				hitbox.damage(attack)
	
	


	
