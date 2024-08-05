extends Control
var main_scene: PackedScene = preload("res://Scenes/stage.tscn")

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_sudoku_button_pressed():
	SceneManager.swap_scenes("res://Scenes/stage.tscn", self, SceneManager.Transitions.FADE)


