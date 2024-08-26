extends CharacterBody2D

class_name Enemy1

var player: CharacterBody2D
var player_seen : bool = false
var crumb_seen: bool = false
var crumb_direction: Vector2


func _ready() -> void:
	player = get_tree().get_first_node_in_group("player")
	$HealthBar.max_value = $HealthComponent.MAX_HEALTH
	$HealthBar.value = $HealthComponent.health

func _physics_process(delta: float) -> void:
	move_and_collide(velocity * delta)
	
	var player_direction = player.global_position - global_position
	var crumb = get_tree().get_first_node_in_group("crumbs")
	
	if crumb:
		crumb_direction = crumb.global_position - global_position
		
		for ray in $CrumbRay.get_children():
			ray.rotation = crumb_direction.angle()
			

			if ray.get_collider() is Area2D:
				if ray.get_collider().name == "CrumbArea":
					crumb_seen = true
					break
				else:
					crumb_seen = false
	 
	else:
		crumb_seen = false
	$HealthBar.value = $HealthComponent.health
	
	
	
	for ray in $Rays.get_children():
		ray.rotation = player_direction.angle()
	
	
		if ray.get_collider() == player:
			player_seen = true
			break
		else:
			player_seen = false
			
	if player_seen or crumb_seen:
		if $StateMachine.current_state is EnemyIdle:
				$StateMachine.on_child_transition($StateMachine.current_state, "follow")
	else:
		if $StateMachine.current_state is EnemyFollow:
				$StateMachine.on_child_transition($StateMachine.current_state, "idle")
		
		
	if $StateMachine.current_state is EnemyFollow:
		if player_seen:
			$AnimatedSprite2D.rotation = player_direction.angle()
		elif crumb_seen:
			if crumb_direction:
				$AnimatedSprite2D.rotation = crumb_direction.angle()
	else:
		if velocity.length() > 0.1:
			$AnimatedSprite2D.rotation = velocity.angle()
		
