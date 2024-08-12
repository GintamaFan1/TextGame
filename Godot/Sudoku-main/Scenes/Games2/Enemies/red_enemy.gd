extends Node2D

var starting_position: String

# Called when the node enters the scene tree for the first time.
func _ready():
	if position.x <= 10:
		starting_position = "left"
	else:
		starting_position = "right"
	


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if starting_position == "left":
		$".".position += Vector2(135, 0) * delta
		$AnimationPlayer.play("Rotate")
	elif starting_position == "right":
		$".".position -= Vector2(135, 0) * delta
		$AnimationPlayer.play("Reverse")

