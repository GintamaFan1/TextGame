extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0
var vacuuming: bool = false
var pushing: bool = false
var limit_reached :bool = false

@onready var vacuume: PackedScene = preload("res://Scenes/Games2/Abilities/Vacumme.tscn")
@onready var pusher: PackedScene = preload("res://Scenes/Games2/Abilities/wave.tscn")

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
		
	if vacuuming == false and pushing == false:	
		look_at(get_global_mouse_position())
		
	if vacuuming == true and limit_reached == false:
		Sucker.lung_capacity -= 10 * delta
	elif pushing == true and limit_reached == false:
		Sucker.lung_capacity -= 10 * delta
	elif limit_reached == true:
		slow_recharge(delta)
	else:
		recharging(delta)
	
	
	
	
	
	if Input.is_action_pressed("Click") and limit_reached == false:
		suck()
	if Input.is_action_just_released("Click") or limit_reached:
		vacuuming = false
		var vortex = get_tree().get_first_node_in_group("vortex")
		if vortex:
			vortex.queue_free()
	
	if Input.is_action_pressed("R_click") and limit_reached == false:
		push()
	if Input.is_action_just_released("R_click") or limit_reached:
		pushing = false
		var wave = get_tree().get_first_node_in_group("wave")
		if wave:
			wave.queue_free()
		
	if Sucker.lung_capacity <= 1:
		limit_reached = true
		
	
func suck():
	vacuuming = true
	if not get_tree().has_group("vortex"):
		var vortex = vacuume.instantiate()
		vortex.add_to_group("vortex")
		vortex.position = position
		vortex.rotation_degrees = rotation_degrees
		
		get_parent().add_child(vortex)
	
	if limit_reached == true:
		return
func push():
	pushing = true
	if not get_tree().has_group("wave"):
		
		var wave = pusher.instantiate()
		wave.add_to_group("wave")
		wave.position = position
		wave.rotation_degrees = rotation_degrees
		
		get_parent().add_child(wave)
	
	if limit_reached == true:
		return
	

func _on_area_2d_body_entered(body):
	
	if "enemy" in body.name.to_lower():
		Sucker.character_health -= Sucker.ENEMY_DAMAGE
		body.explode()

func recharging(delta):
	if Sucker.lung_capacity < Sucker.original_lung_capacity:
		Sucker.lung_capacity += 7 * delta
	if Sucker.lung_capacity > Sucker.original_lung_capacity:
		Sucker.lung_capacity = Sucker.original_lung_capacity

func slow_recharge(delta):
	if Sucker.lung_capacity <= 20:
		Sucker.lung_capacity += 3 * delta
	
	if Sucker.lung_capacity > 20:
		limit_reached = false
	
	
