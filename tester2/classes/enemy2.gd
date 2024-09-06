extends StaticBody2D

class_name Enemy2
signal died()

var player: CharacterBody2D
var player_direction: Vector2
var player_seen: bool = false
var player_loaded: bool = false
var respawn_timer: Timer
@onready var cross_hairs_scene : PackedScene = preload("res://scenes/cross_hairs.tscn")



var cross_hairs
var in_path: bool = false

func _ready() -> void:
	player = get_tree().get_first_node_in_group("player")
	cross_hairs = cross_hairs_scene.instantiate()
	player_loaded = false
	player_seen = false
	

func _physics_process(_delta: float) -> void:
	if not player_loaded:
		player = get_tree().get_first_node_in_group("player")
		player_loaded = true
		
	if player:
		player_direction = player.global_position - global_position
	
	
	for ray: RayCast2D in $TrackingRay.get_children():
		if player_direction:
			ray.rotation = player_direction.angle()
		
		
		if ray.get_collider() == player:
			player_seen = true
			break
		else:
			player_seen = false
	
	
	
	if player_seen == true:
		if $StateMachine.current_state is SentryIdle:
			print("switching to aim")
			$StateMachine.on_child_transition($StateMachine.current_state, "aim")
	else:
		if $StateMachine.current_state is SentryAim:
			print("to idle")
			$StateMachine.on_child_transition($StateMachine.current_state, "idle")
		if cross_hairs:
			if in_path == true:
				player.remove_child(cross_hairs)
				in_path = false
		
	if $StateMachine.current_state is SentryAim:
		if player_seen:
			$Sprite2D.rotation = player_direction.angle()
			if cross_hairs != null:
				if in_path == false:
					
					player.add_child(cross_hairs)
					in_path = true

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
	
	
