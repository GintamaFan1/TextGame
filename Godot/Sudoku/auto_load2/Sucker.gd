extends Node

var  character_health = 100
var orignal_character_health = 100
var train_health = 200
var original_train_health = 200
const ENEMY_DAMAGE = 20
var lung_capacity = 120
var original_lung_capacity = 120
var game_over_info : Dictionary = {}
var selected_stage_path = null
var next_stage_path = null
var score: int = 0
var high_score = 0
var code_executed = false
var test_speed = 1


func score_reset():
	var dir = DirAccess.open("user://")
	var stage =  game_over_info["stage_name"]
	
	if not dir.dir_exists(stage):
		dir.make_dir(stage)
		
	dir.change_dir(stage)
	
	dir.list_dir_begin()
	
	var file = dir.get_next()
	
	if file == stage + ".save":
		var err = dir.remove(file)
		
		
	

func update_score():
	score = (character_health + train_health) * 100
	score_reset()
	if game_over_info["game_won"] == true:
		var dir = DirAccess.open("user://")
		var stage =  game_over_info["stage_name"]
		
		if not dir.dir_exists(stage):
			dir.make_dir(stage)
			
		dir.change_dir(stage)
		
		var file_path = "user://" + stage +"/" + stage + ".save"
		
		if FileAccess.file_exists(file_path):
			var save_file = FileAccess.open(file_path, FileAccess.READ_WRITE)
			var json_string = save_file.get_as_text()
			
			var save_data = JSON.parse_string(json_string)
			
			if save_data == null:
				DisplayMessage.display_alert_message("Error getting save file")
				return
			
			var old_score = save_data["score"]
			
			if old_score >= score:
				save_file.close()
				return
			else:
				save_data["score"] = score
				save_file.store_string(JSON.stringify(save_data))
				save_file.close()
				return
		else:
			var save_file = FileAccess.open(file_path, FileAccess.WRITE)
			var save_data: Dictionary = {
				"score": score
			}
			
			save_file.store_string(JSON.stringify(save_data))
			save_file.close()
			
func get_highscore():
	if game_over_info["game_won"] == true:
		var dir = DirAccess.open("user://")
		var stage =  game_over_info["stage_name"]
		
		if not dir.dir_exists(stage):
			dir.make_dir(stage)
			
		dir.change_dir(stage)
		
		var file_path = "user://" + stage +"/" + stage + ".save"
		
		if FileAccess.file_exists(file_path):
			var save_file = FileAccess.open(file_path, FileAccess.READ )
			var json_string = save_file.get_as_text()
			
			save_file.close()
			
			var save_data = JSON.parse_string(json_string)
			
			if save_data == null:
				DisplayMessage.display_alert_message("Error getting save file")
				return
			
			high_score = save_data["score"]
	
	
	
	
