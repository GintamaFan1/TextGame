extends CharacterBody2D


const SPEED = 200.0
const JUMP_VELOCITY = -400.0
var attacking: bool = false
var knock_back: float = 100
var attack_damage:float = 10
var stun_time: float = 0.5
var crumb_scene: PackedScene = preload("res://scenes/bread_crumb.tscn")
var is_stunned: bool = false
var slash = null
var slash_scene: PackedScene = preload("res://scenes/slash.tscn")
var bag:Bag = Bag.new()



func _ready():
	$CrumbTimer.start()


func _physics_process(delta: float) -> void:
	
	if slash == null:
		slash = slash_scene.instantiate()
		slash.hitbox_hit.connect(_slash_hit)
	var direction = Input.get_vector("left","right","up","down")
	
	if is_stunned == false:
		position += direction * SPEED * delta
	
	
	
	move_and_collide(velocity * delta)
	
	look_at(get_global_mouse_position())
	
	if Input.is_action_pressed("basic_attack") and is_stunned == false:
		$AnimatedSprite2D.play("attack")
		
			
		if $AnimatedSprite2D.frame > 1:
			_attack(slash)
		if $AnimatedSprite2D.frame == 3:
			Input.action_release("basic_attack")

	else:
		$AnimatedSprite2D.play("idle")
		
	
	if Input.is_action_just_released("basic_attack"):
		if slash != null:
			slash.queue_free()
	
	if Input.is_action_just_pressed("scroll up"):
		$Camera2D.zoom.x += 1
		$Camera2D.zoom.x = clamp($Camera2D.zoom.x, 2, 7)
		$Camera2D.zoom.y += 1
		$Camera2D.zoom.y = clamp($Camera2D.zoom.y, 2, 7)
		
		


	if Input.is_action_just_pressed("scroll down"):
		$Camera2D.zoom.x -= 1
		$Camera2D.zoom.x = clamp($Camera2D.zoom.x, 2, 7)
		$Camera2D.zoom.y -= 1
		$Camera2D.zoom.y = clamp($Camera2D.zoom.y, 2, 7)

		


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

func _slash_hit(body):
	if attacking:
		if body is Enemy1:
			
			var enemy_hitbox = body.get_node("HitboxComponent")
			
			if enemy_hitbox:
				var attack = Attack.new()
				attack.attack_damage = attack_damage
				attack.stun_time = stun_time
				attack.knock_back = knock_back 
				attack.attacker = self
				attack.attacked_enemy = body
				enemy_hitbox.damage(attack)
				
		elif body is Objects:
			var enemy_hitbox = body.get_node("HitboxComponent")
			
			if enemy_hitbox:
				var attack = Attack.new()
				attack.attack_damage = attack_damage
				attack.stun_time = stun_time
				attack.knock_back = knock_back 
				attack.attacker = self
				attack.attacked_object = body
				enemy_hitbox.damage(attack)
		elif body is Enemy2:
			var enemy_hitbox = body.get_node("HitboxComponent")
			
			if enemy_hitbox:
				var attack = Attack.new()
				attack.attack_damage = attack_damage
				attack.stun_time = stun_time
				attack.knock_back = knock_back 
				attack.attacker = self
				attack.attacked_enemy = body
				enemy_hitbox.damage(attack)
			

func _attack(slash1):
	attacking = true
	if not has_node("slash") and slash1 != null:
		add_child(slash1)

	
func on_pickup(item: Item):
	bag.add_item(item)
