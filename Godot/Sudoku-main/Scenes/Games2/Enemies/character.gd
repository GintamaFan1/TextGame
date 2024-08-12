extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0
var vacuuming: bool = false

@onready var vacuume: PackedScene = preload("res://Scenes/Games2/Abilities/Vacumme.tscn")

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/2d/default_gravity")


func _physics_process(delta):
	# Add the gravity.


	# Handle jump.
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var direction = Input.get_axis("ui_left", "ui_right")
	if direction:
		velocity.x = direction * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		
	if vacuuming == false:	
		look_at(get_global_mouse_position())
	

	
	

	move_and_slide()
	
	if Input.is_action_pressed("Click"):
		suck()
	if Input.is_action_just_released("Click"):
		vacuuming = false
		var vortex = get_tree().get_first_node_in_group("vortex")
		vortex.queue_free()
		
		
	
func suck():
	vacuuming = true
	if not get_tree().has_group("vortex"):
		var vortex = vacuume.instantiate()
		vortex.add_to_group("vortex")
		vortex.position = position
		vortex.rotation_degrees = rotation_degrees
		
		get_parent().add_child(vortex)
	
	
	
