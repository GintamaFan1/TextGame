extends CanvasLayer

var character_scene: PackedScene = preload("res://scenes/character.tscn")
var health_box: HealthComponent
var character_called: bool = false


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	%RedQuartzLabel.text = str(Inventory.red_quartz)
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var character = get_tree().get_first_node_in_group("player")
	if character and not character_called:
		health_box = character.get_node("HealthComponent")
		%CharacterHealthBar.max_value = health_box.MAX_HEALTH
		%CharacterHealthBar.value = health_box.MAX_HEALTH
		health_box.health_changed.connect(_update_health)
		character_called = true
	Inventory.blocks_changed.connect(_update_materials)

func _update_health(health):
	if health_box:
		%CharacterHealthBar.value = health_box.health
	
func _update_materials():
	%RedQuartzLabel.text = str(Inventory.red_quartz)
	
