extends State

class_name EnemyAttack

@export var enemy: CharacterBody2D
var player : CharacterBody2D
var animated_sprite: AnimatedSprite2D

func Enter():
	
	player = get_tree().get_first_node_in_group("player")
	animated_sprite = enemy.get_node("AnimatedSprite2D")
	animated_sprite.play("idle")
	
func Physics_Update(_delta: float):
	var direction = player.global_position - enemy.global_position
	
	
	animated_sprite.rotation = direction.angle()
	
	animated_sprite.play("attack")
	await animated_sprite.animation_finished
	
	Transitioned.emit(self, "follow")
	
	
