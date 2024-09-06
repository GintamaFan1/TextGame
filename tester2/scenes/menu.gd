extends Control

var level1_scene: PackedScene = preload("res://scenes/level.tscn")
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	pass


func _on_close_button_pressed() -> void:
	get_tree().paused = false
	$".".queue_free()


func _on_save_button_pressed() -> void:
	SaveManager.slot = $Panel/VBoxContainer/SlotButton.selected
	Inventory.save_blocks()
	SaveManager.save_character()


func _on_load_button_pressed() -> void:
	SaveManager.slot = $Panel/VBoxContainer/SlotButton2.selected
	get_tree().paused = false
	get_tree().change_scene_to_file("res://scenes/level.tscn")
	$".".queue_free()


func _on_delete_button_pressed() -> void:
	SaveManager.slot = $Panel/VBoxContainer/SlotButton3.selected
	SaveManager.delete_save()
