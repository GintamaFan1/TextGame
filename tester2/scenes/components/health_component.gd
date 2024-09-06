extends Node2D

class_name HealthComponent

@export var MAX_HEALTH: float 
var health: float = 0

signal health_changed(health)

func _ready() -> void:
	if health == 0:
		health = MAX_HEALTH
	
func damage(attack:Attack):
	print(health)
	health -= attack.attack_damage
	if get_parent().name == "Character":
		health_changed.emit(health)
	if get_parent() is CharacterBody2D or get_parent() is RigidBody2D:
		if attack.attacked_enemy:
			var direction = attack.attacker.global_position - attack.attacked_enemy.global_position
			var push = direction.normalized() * attack.knock_back
			get_parent().velocity -= push
			var stun_timer = Timer.new()
			get_parent().is_stunned = true
			stun_timer.wait_time = attack.stun_time
			
			stun_timer.one_shot = true
			get_parent().add_child(stun_timer)
			stun_timer.start()
			stun_timer.timeout.connect(knockback)
	
	if health <= 0:
		if get_parent() is Objects:
			get_parent().release_quartz()
		if get_parent() is Enemy1 or get_parent() is Enemy2:
			var parent = get_parent()
			print("trying to emit")
			parent.died.emit()
		get_parent().queue_free()

func knockback():
	
	get_parent().velocity = Vector2.ZERO
	get_parent().is_stunned = false
