extends Node2D


var enemy1_scene: PackedScene = preload("res://scenes/enemy_1.tscn")
var cannon_scene: PackedScene = preload("res://scenes/cannon.tscn")
var character_scene: PackedScene = preload("res://scenes/character.tscn")
var tally: int = 0

func _ready() -> void:
	var character_data:PlayerData = SaveManager.load_character()
	var character = character_scene.instantiate()
	
	
	%CharacterStart.add_child(character)
	
	
	if character_data != null:
		get_tree().call_group("game_events", "on_before_load_game")
		var health_box = character.get_node("HealthComponent")
		health_box.health = character_data.health
		
		character.global_position = character_data.position
		var camera: Camera2D = get_tree().get_first_node_in_group("player_camera")
		camera.zoom = character_data.zoom
		
		for item in character_data.save_data:
			var scene = load(item.scene_path) as PackedScene
			var restored_node = scene.instantiate()
			
			if restored_node is Enemy1:
			
				for marker in $StarterMarkers.get_children():
					
					if marker.name == item.parent_name:
						restored_node.name = "enemy" + str(tally)
						restored_node.died.connect(respawn.bind(marker,enemy1_scene))
						marker.add_child(restored_node)
						tally += 1
		
			elif restored_node is Enemy2:
			
				for marker in $Cannons.get_children():
					if marker.name == item.parent_name:
						restored_node.name = "enemy" + str(tally)
						restored_node.died.connect(respawn.bind(marker, enemy1_scene))
						marker.add_child(restored_node)
						tally += 1
			else:
				add_child(restored_node)
			
			
			if restored_node.has_method("on_load_game"):
				restored_node.on_load_game(item)
			
		for marker in $StarterMarkers.get_children():
			if marker.get_child_count() == 0:
				respawn(marker, enemy1_scene)
		
		for marker in $Cannons.get_children():
			if marker.get_child_count() == 0:
				respawn(marker, cannon_scene)
		
	else:
		character.position = %CharacterStart.global_position
		
		for marker in $StarterMarkers.get_children():
			var enemy1:Enemy1 = enemy1_scene.instantiate()
			enemy1.name = "enemy" + str(tally)
			enemy1.position = marker.global_position
			enemy1.died.connect(respawn.bind(marker,enemy1_scene))
			marker.add_child(enemy1)
			tally += 1
		
		for marker in $Cannons.get_children():
			var enemy2: Enemy2 = cannon_scene.instantiate()
			enemy2.name = "enemy" + str(tally)
			enemy2.position = marker.global_position
			enemy2.died.connect(respawn.bind(marker, cannon_scene))
			marker.add_child(enemy2)
			tally += 1

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass
	

func respawn(marker:Marker2D, enemy_scene:PackedScene):
	print("respawning called")
	var timer:Timer = Timer.new()
	timer.wait_time = 30
	timer.one_shot = true
	timer.autostart = true
	timer.timeout.connect(respawning_finished.bind(marker, enemy_scene, timer))
	add_child(timer)
	

func respawning_finished(marker:Marker2D, enemy_scene:PackedScene, timer:Timer):
	timer.queue_free()
	var enemy1 = enemy_scene.instantiate()
	marker.add_child(enemy1)
	
	
	
		
