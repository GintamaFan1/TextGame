extends Control


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	pass


func _on_stage_1_button_pressed():
	Sucker.selected_stage_path = "res://Scenes/Games2/Stage/stage_1.tscn"
	


func _on_stage_2_button_pressed():
	Sucker.selected_stage_path = "res://Scenes/Games2/Stage/stage_2.tscn"


func _on_stage_3_button_pressed():
	Sucker.selected_stage_path = "res://Scenes/Games2/Stage/stage_3.tscn"
