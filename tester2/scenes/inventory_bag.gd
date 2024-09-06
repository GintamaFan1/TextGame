extends PanelContainer
class_name InventoryBag

@export var slot_scene: PackedScene
@onready var grid_container: GridContainer = %GridContainer

func open(bag:Bag):
	
	show()
	
	for child in grid_container.get_children():
		child.queue_free()
	
	for item in bag.get_items():
		var slot = slot_scene.instantiate()
		grid_container.add_child(slot)
		slot.display(item)

func _on_close_button_pressed() -> void:
	hide()
