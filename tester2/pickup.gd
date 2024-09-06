extends Node2D

@export var item:Item
@onready var sprite_2d: Sprite2D = %Sprite2D

func _ready() -> void:
	var item = item.scene.instantiate()
	add_child(item)



func _on_area_2d_body_entered(body: Node2D) -> void:
	if body.has_method("on_pickup"):
		body.on_pickup(item)
		queue_free()
