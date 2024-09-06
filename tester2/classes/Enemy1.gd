extends CharacterBody2D

class_name Enemy1
signal died()

var player: CharacterBody2D
var player_seen : bool = false
var crumb_seen: bool = false
var crumb_direction: Vector2
var player_direction: Vector2
var is_stunned: bool = false
var charging: bool = false
var respawn_timer: Timer


func _ready() -> void:
	player = get_tree().get_first_node_in_group("player")
	$HealthBar.max_value = $HealthComponent.MAX_HEALTH
	$HealthBar.value = $HealthComponent.health
	
	
	
	

func _physics_process(delta: float) -> void:
	move_and_collide(velocity * delta)
	
		
	
	if player:
		var player_global_position = player.global_position
		var enemy_global_position = global_position
		player_direction = player_global_position - enemy_global_position
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
		if player_direction:
			ray.rotation = player_direction.angle()
	
	
		if ray.get_collider() == player:
			player_seen = true
			break
		else:
			player_seen = false
			
			
	if is_stunned == false:
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
		
func attack(_player):
	pass
func recharged():
	charging = false
	
func on_save_game(save_data:Array[SavedData]):
	var data = SavedData.new()
	
	data.position = global_position
	data.scene_path = scene_file_path
	data.health = $HealthComponent.health
	data.parent_name = get_parent().name
	
	
	save_data.append(data)
	
func on_before_load_game():
	get_parent().remove_child(self)
	queue_free()
	
func on_load_game(data):

	global_position = data.position
	$HealthComponent.health = data.health
	
	
	
