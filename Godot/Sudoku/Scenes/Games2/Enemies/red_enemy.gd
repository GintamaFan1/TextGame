extends CharacterBody2D

var starting_direction: String
var original_direction: String
var speed = 135
var original_speed: float
var starting_speed : float
var slowed_speed: float = starting_speed / 2

# Called when the node enters the scene tree for the first time.
func _ready():
	if position.x <= 200:
		starting_direction = "right"
	else:
		starting_direction = "left"
	
	original_direction = starting_direction
	original_speed = speed

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _physics_process(delta):
	if starting_direction == "right":
		move_right(delta)
	elif starting_direction == "left":
		move_left(delta)
	

func explode():
	queue_free()

func move_right(delta):
	position.x += speed * delta
	$AnimationPlayer.play("Rotate")
	starting_speed = $AnimationPlayer.get_playing_speed()
	
func move_left(delta):
	position.x -= speed * delta
	$AnimationPlayer.play("Reverse")
	starting_speed = $AnimationPlayer.get_playing_speed()

func slow():
	$AnimationPlayer.speed_scale = starting_speed / 2.5
	
func unslow():
	$AnimationPlayer.speed_scale = starting_speed
