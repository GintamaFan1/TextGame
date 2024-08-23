extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	$Panel/VBoxContainer/Label.text = $Panel/VBoxContainer/Label.text + str(Sucker.high_score)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_previous_button_pressed():
	var info = Sucker.game_over_info
	var stage = info["stage"]
	
	Sucker.selected_stage_path = stage
	
	


func _on_next_button_pressed():
	var info = Sucker.game_over_info
	var stage_name = info["stage"][32]
	print(stage_name)
	var num = int(stage_name)
	print(num)
	var scene_path = "res://Scenes/Games2/Stage/stage_" + str(num + 1) + ".tscn"
	print(scene_path)
	if ResourceLoader.exists(scene_path):
		Sucker.selected_stage_path = scene_path
	
