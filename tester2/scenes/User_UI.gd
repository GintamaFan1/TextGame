extends CanvasLayer

var character_scene: PackedScene = preload("res://scenes/character.tscn")
var menu_scene: PackedScene = preload("res://scenes/menu.tscn")
var health_box: HealthComponent
var character_called: bool = false
var menu: Control
var character: CharacterBody2D

@onready var inventory_bag: InventoryBag = %InventoryBag


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	%RedQuartzLabel.text = str(Inventory.red_quartz)
	Inventory.blocks_changed.connect(_update_materials)
	
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta: float) -> void:
	character = get_tree().get_first_node_in_group("player")
	if character and not character_called:
		health_box = character.get_node("HealthComponent")
		%CharacterHealthBar.max_value = health_box.MAX_HEALTH
		%CharacterHealthBar.value = health_box.health
		health_box.health_changed.connect(_update_health)
		character_called = true
	

func _update_health(health):
	if health_box:
		%CharacterHealthBar.value = health_box.health
	
func _update_materials():
	%RedQuartzLabel.text = str(Inventory.red_quartz)


func _on_menu_button_gg_pressed() -> void:
	if not menu:
		get_tree().paused = true
		menu = menu_scene.instantiate()
		
		$".".add_child(menu)

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_released("open bag"):
		inventory_bag.open(character.bag)
		
		
