extends CharacterBody2D


const SPEED = 300.0
const JUMP_VELOCITY = -400.0
var attacking: bool = false

var attack_damage = 10
var crumb_scene: PackedScene = preload("res://scenes/bread_crumb.tscn")

func _ready():
	$CrumbTimer.start()


func _physics_process(delta: float) -> void:
	
	var direction = Input.get_vector("left","right","up","down")
	position += direction * SPEED * delta
	
	move_and_collide(velocity * delta)
	
	look_at(get_global_mouse_position())
	
	if Input.is_action_pressed("basic_attack"):
		$AnimatedSprite2D.play("attack")
		attacking = true
		await $AnimatedSprite2D.animation_finished
		attacking = false

	else:
		$AnimatedSprite2D.play("idle")
		attacking = false


func _on_hitbox_component_body_entered(body: Node2D) -> void:
	if body is Enemy1 and attacking == true:
		
		var enemy_hitbox = body.get_node("HitboxComponent")
		
		if enemy_hitbox:
			var attack = Attack.new()
			attack.attack_damage = attack_damage
			attack.stun_time = 0
			enemy_hitbox.damage(attack)
			
			


func _on_crumb_timer_timeout() -> void:
	
	var enemies = get_tree().get_nodes_in_group("enemies")
	
	for ene in enemies:
		if ene.player_seen == true:
			var crumb = crumb_scene.instantiate()
			var stages = get_tree().get_nodes_in_group("stages")
			for stage in stages:
	
				if stage.name == "level1":
					crumb.position = global_position
					
					stage.add_child(crumb)
					break
			
			break
