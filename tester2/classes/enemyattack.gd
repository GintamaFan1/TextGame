extends State

class_name EnemyAttack

@export var enemy: CharacterBody2D
var player : CharacterBody2D
var animated_sprite: AnimatedSprite2D
var timer: Timer

func Enter():
	
	player = get_tree().get_first_node_in_group("player")
	animated_sprite = enemy.get_node("AnimatedSprite2D")
	animated_sprite.play("idle")
	var recharge = enemy.get_node("RechargeComponent")
	timer = recharge.get_node("Timer")
	timer.start()
	
func Physics_Update(_delta: float):
	var direction = player.global_position - enemy.global_position
	enemy.velocity = Vector2.ZERO
	
	animated_sprite.rotation = direction.angle()
	
	animated_sprite.play("attack")
	enemy.attack(player)
	await animated_sprite.animation_finished
	enemy.charging = true
	
	
	Transitioned.emit(self, "follow")
	
	
