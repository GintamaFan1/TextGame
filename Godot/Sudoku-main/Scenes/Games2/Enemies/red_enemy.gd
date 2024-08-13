extends CharacterBody2D

var starting_direction: String
var original_direction: String
var speed = 135
var original_speed: float

# Called when the node enters the scene tree for the first time.
func _ready():
	if position.x <= 200:
		starting_direction = "right"
	else:
		starting_direction = "left"
	
	original_direction = starting_direction
	original_speed = speed

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if starting_direction == "right":
		position.x += speed * delta
		$AnimationPlayer.play("Rotate")
	elif starting_direction == "left":
		position.x -= speed * delta
		$AnimationPlayer.play("Reverse")
	else:
		$AnimationPlayer.pause()
		
	if speed < original_speed:
		starting_direction = "stopped"
		
	else:
		starting_direction = original_direction

func explode():
	queue_free()
