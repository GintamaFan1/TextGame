extends Enemy1
class_name Ranger

var attack_damage:float = 10
var knock_back:float  = 50
var stun_time: float = .7

func attack(player1):
	var attack1 = Attack.new()
	
	attack1.attack_damage = attack_damage
	attack1.knock_back = knock_back
	attack1.stun_time = stun_time
	attack1.attacker = self
	attack1.attacked_enemy = player

	if player1.name == "Character":
		if player1.has_node("HitboxComponent"):
			var hitbox = player.get_node("HitboxComponent")
			if hitbox:
				hitbox.damage(attack1)
	
	


	
