extends CharacterBody2D

class_name Monsters

const speed = 50
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")

func _ready():
	pass

func _physics_process(delta):
	if not is_on_floor():
		velocity.y += gravity * delta
	
	var direction = Input.get_vector("left", "right", "up", "down")
	position += direction * speed * delta
	
	if direction.x < 0:
		$AnimatedSprite2D.flip_h = true
		
	else:
		$AnimatedSprite2D.flip_h = false
		
	
		
	if Input.is_action_pressed("attack"):
		$AnimatedSprite2D.play("attack")
	
	elif direction.x < 0 or direction.x > 0:
		$AnimatedSprite2D.play("walk")
	else:
		$AnimatedSprite2D.play("idle")
		
	
	move_and_slide()
