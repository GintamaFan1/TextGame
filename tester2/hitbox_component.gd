extends Area2D
class_name HitboxComponent

@export var health_component: HealthComponent
var vulnerable :bool = true

func _ready():
	if get_parent().has_node("AnimatedSprite2D"):
		var sprite = get_parent().get_node("AnimatedSprite2D")
		if sprite.material:
			sprite.material = sprite.material.duplicate()

func damage(attack:Attack):
	if health_component:
		if vulnerable == true:
			health_component.damage(attack)
			vulnerable = false
			$vulnerability.start()
			if get_parent().has_node("AnimatedSprite2D"):
				var sprite = get_parent().get_node("AnimatedSprite2D")
				sprite.material.set_shader_parameter("progress", 1)
					
			


func _on_vulnerability_timeout() -> void:
	vulnerable = true
	if get_parent().has_node("AnimatedSprite2D"):
		var sprite = get_parent().get_node("AnimatedSprite2D")
		if sprite.material:
			sprite.material.set_shader_parameter("progress", 0)
		else:
			print("no material")
