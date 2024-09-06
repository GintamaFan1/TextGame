extends Enemy2

@onready var cannon_ball_scene: PackedScene = preload("res://scenes/cannonball.tscn")

func attack():
	print("calling ball")
	var ball = cannon_ball_scene.instantiate()
	
	
	
	ball.global_position = global_position
	
	get_tree().root.add_child(ball)
	
	
