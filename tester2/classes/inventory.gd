extends Node



var red_quartz: int = 0
var blue_quartz: int = 0
signal blocks_changed

func _ready() -> void:
	
	load_blocks()
	

func save_blocks():
	
	var quartz = BuildingBlocks.new()
	quartz.red_quartz = red_quartz
	quartz.blue_quartz = blue_quartz
	SaveManager.save_blocks(quartz, "quartz")
	load_blocks()
	
	

func load_blocks():
	var quartz = BuildingBlocks.new()
	var resource = SaveManager.load_blocks("quartz")
	red_quartz = resource.red_quartz
	blue_quartz = resource.blue_quartz
	blocks_changed.emit()
