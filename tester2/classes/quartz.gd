extends Node2D

class_name Quartz

signal materials_added

var area: Area2D
func _ready():

	area = $Sprite2D/Area2D
	area.body_entered.connect(player_entered)


func player_entered(body: Node2D):
	if body.name == "Character":
		if self is BlueQuartz:
			Inventory.blue_quartz += 1
		elif self is RedQuartz:
			Inventory.red_quartz += 1
		Inventory.save_blocks()
		
		queue_free()
