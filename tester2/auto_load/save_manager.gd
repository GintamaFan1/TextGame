extends Node

var save_folder = "saves/"
var open_dir = "user://"
func _ready():
	var dir = DirAccess.open(open_dir)
	if not dir.dir_exists(save_folder):
		dir.make_dir_recursive(save_folder)
	
	dir.change_dir("saves")
	dir.list_dir_begin()
	
	var file = dir.get_next()
	while file != "":
		
		print(file)
	
		file = dir.get_next()

func get_save_path(filename: String) -> String:
	return open_dir + save_folder + filename
	
func save_blocks(resource: Resource, filename: String):
	ResourceSaver.save(resource,"user://" + save_folder + filename + ".tres")
	
func load_blocks(filename: String):

	var resource = ResourceLoader.load( "user://" + save_folder + filename + ".tres")
	return resource
