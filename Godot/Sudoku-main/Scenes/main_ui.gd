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
	$CanvasLayer/Settings.visible = true
	
func drag(event):
	if Input.is_action_pressed("Drag"):
		if event is InputEventMouseMotion:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, -2000,2000)
			new_position.y = clamp(new_position.y, -2000, 2000)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
		elif event is InputEventScreenDrag:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, -2000,2000)
			new_position.y = clamp(new_position.y, -2000, 2000)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
		
	else:
		dragging = false
	
	if Input.is_action_pressed("Click"):
		if event is InputEventScreenDrag:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, -2000,2000)
			new_position.y = clamp(new_position.y, -2000, 2000)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
	else:
		dragging = false
			
func _input(event):
	drag(event)
