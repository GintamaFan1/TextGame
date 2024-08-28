extends State

class_name EnemyFollow

@export var enemy: CharacterBody2D
@export var move_speed := 40.0
var player: CharacterBody2D
var animated_sprite: AnimatedSprite2D
var crumb_direction: Vector2

func Enter():
	player = get_tree().get_first_node_in_group("player")
	animated_sprite = enemy.get_node("AnimatedSprite2D")
	animated_sprite.play("idle")
func Physics_Update(_delta: float):
	var direction = player.global_position - enemy.global_position
	var crumb = get_tree().get_first_node_in_group("crumbs")
	
	
	if enemy.is_stunned == false:
		if direction.length() > 30:
			enemy.velocity = direction.normalized() * move_speed
		else:            
			Transitioned.emit(self, "attack")
			
		
		if crumb:
			crumb_direction = crumb.global_position - enemy.global_position
			if enemy.crumb_seen == true and enemy.player_seen == false:
				if crumb_direction:
					enemy.velocity = crumb_direction.normalized() * move_speed
					
		if direction.length() > 200 and enemy.crumb_seen == false:
			Transitioned.emit(self, "idle")
		if direction.length() > 200 and enemy.crumb_seen:
			if crumb_direction:
					enemy.velocity = crumb_direction.normalized() * move_speed
