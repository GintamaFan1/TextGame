extends Node

var save_folder = "saves/"
var open_dir = "user://"
var slot: int = 0

func _ready():
	
	var dir = DirAccess.open(open_dir)
	if not dir.dir_exists(save_folder):
		dir.make_dir_recursive(save_folder)
	
	dir.change_dir("saves")
	

func get_save_path(filename: String) -> String:
	return open_dir + save_folder + filename
	
func save_blocks(resource: Resource, filename: String):
	ResourceSaver.save(resource,"user://" + save_folder + filename + ".tres")
	
func load_blocks(filename: String):

	var resource = ResourceLoader.load( "user://" + save_folder + filename + ".tres")
	return resource

func save_character():
	var player:CharacterBody2D = get_tree().get_first_node_in_group("player")
	if player:
		var data = PlayerData.new()
		var health_box = player.get_node("HealthComponent")
		data.position = player.global_position
		data.health = health_box.health
		data.zoom = get_tree().get_first_node_in_group("player_camera").zoom
		
		var saved_data:Array[SavedData] = []
		
		get_tree().call_group("game_events", "on_save_game", saved_data)
		data.save_data = saved_data
		
		ResourceSaver.save(data, "user://saves/player" + str(slot) + ".tres")
	
	

func load_character():
	var data = PlayerData.new()
	data = ResourceLoader.load("user://saves/player" + str(slot) + ".tres") as PlayerData
	return data
	
func delete_save():

	var dir = DirAccess.open("user://saves/")
	if not FileAccess.file_exists("user://saves/player" + str(slot) + ".tres"):
		print("not found")
		return
	
	else:
		dir.list_dir_begin()
		var file = dir.get_next()
		
		while file != "":
			print(file)
			
			file = dir.get_next()
		var err = dir.remove("user://saves/player" + str(slot) + ".tres")
		print(err)
	
	
