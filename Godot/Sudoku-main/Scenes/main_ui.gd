extends Node2D

var negative_clamp = -1
var positive_clamp_x = 1800
var positive_clamp_y = 1600


@onready var dragging : bool = false
# Called when the node enters the scene tree for the first time.
func _ready():
	$CanvasLayer2/Camera2D.make_current()
	
	
	
		


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	if Input.is_action_just_pressed("scroll"):
		var new_position = $CanvasLayer2/Camera2D.position + Vector2(0, 15)
		new_position.y = clamp(new_position.y, negative_clamp, positive_clamp_y)
		
		$CanvasLayer2/Camera2D.position = new_position
	if Input.is_action_just_pressed("scroll down"):
		var new_position = $CanvasLayer2/Camera2D.position + Vector2(0, -15)
		new_position.y = clamp(new_position.y, negative_clamp, positive_clamp_y)
		$CanvasLayer2/Camera2D.position = new_position
	
	


func _on_return_button_pressed():
	SceneManager.change_scene("res://Scenes/main_ui.tscn")


func _on_settingbutton_pressed():
	$CanvasLayer/Settings.visible = true
	
func drag(event):
	if Input.is_action_pressed("Drag"):
		if event is InputEventMouseMotion:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, negative_clamp, positive_clamp_x)
			new_position.y = clamp(new_position.y, negative_clamp, positive_clamp_y)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
		elif event is InputEventScreenDrag:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, negative_clamp, positive_clamp_x)
			new_position.y = clamp(new_position.y, negative_clamp, positive_clamp_y)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
		
	else:
		dragging = false
	
	if Input.is_action_pressed("Click"):
		if event is InputEventScreenDrag:
			var new_position = $CanvasLayer2/Camera2D.position - event.relative
			
			new_position.x = clamp(new_position.x, negative_clamp, positive_clamp_x)
			new_position.y = clamp(new_position.y, negative_clamp, positive_clamp_y)
			
			$CanvasLayer2/Camera2D.position = new_position
			dragging = true
	else:
		dragging = false
			
func _input(event):
	drag(event)
