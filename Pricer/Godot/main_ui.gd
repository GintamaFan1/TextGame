extends Node2D

@onready var dragging : bool = false
# Called when the node enters the scene tree for the first time.
func _ready():
	$CanvasLayer2/Camera2D.make_current()
	
	
	
		


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	if Input.is_action_just_pressed("scroll"):
		$CanvasLayer2/Camera2D.position += Vector2(0,15)
	if Input.is_action_just_pressed("scroll down"):
		$CanvasLayer2/Camera2D.position -= Vector2(0,15)
	
	


func _on_return_button_pressed():
	SceneManager.change_scene("res://Scenes/main_ui.tscn")


func _on_settingbutton_pressed():
	$CanvasLayer/Setting.visible = true
	
func drag(event):
	if Input.is_action_pressed("drag"):
		if event is InputEventMouseMotion:
			$CanvasLayer2/Camera2D.position -= event.relative
			dragging = true
		elif event is InputEventScreenDrag:
			$CanvasLayer2/Camera2D.position -= event.relative
			dragging = true
		
	else:
		dragging = false
func _input(event):
	drag(event)
