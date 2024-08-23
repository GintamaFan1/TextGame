extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0


func _physics_process(delta: float) -> void:
	# Add the gravity.
	var direction = Input.get_vector("ui_left","ui_right","ui_up","ui_down")
	position += direction * SPEED * delta
	
	move_and_slide()
	
	look_at(get_global_mouse_position())
