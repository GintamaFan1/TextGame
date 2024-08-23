extends Node2D

class_name HealthComponent

@export var max_health: float = 150.0
var health: float 

func _ready() -> void:
	health = max_health

func take_damage(attack: Attack):
	health -= attack.attack_damage
	
	if health <= 0:
		get_parent().queue_free()
	
	
	
