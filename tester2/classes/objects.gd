extends StaticBody2D


class_name Objects

@onready var red_quartz_scene : PackedScene = preload("res://Quartz/red_quartz.tscn")
@onready var blue_quartz_scene : PackedScene = preload("res://Quartz/blue_quartz.tscn")


var quartz_created: Dictionary = {}


func _ready():
	var quartz = [red_quartz_scene, blue_quartz_scene]
	generate_quartz(quartz)

func generate_quartz(list):
	for quartz in list:
		var amount = randi_range(0,4)
		
		quartz_created.get_or_add(quartz, amount)
		

func release_quartz():
	
	for quartz in quartz_created.keys():
		for i in range(quartz_created[quartz]):
			var quart = quartz.instantiate()
			var random_pos = randf_range(-20,20)
			quart.global_position = global_position + Vector2(random_pos, random_pos)
			get_tree().root.call_deferred("add_child", quart)
		
		
