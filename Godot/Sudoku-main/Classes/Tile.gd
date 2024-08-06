class_name TileClass


class Tile:
	var sprite: Sprite2D
	var rowNumber: int
	var colNumber: int
	var groupNumber: int
	var value: int
	var trueValue: int
	var open: bool = false
	
	func _init(row: int, col: int):
		rowNumber = row
		colNumber = col
		groupNumber = get_quadrant(row, col)
		value = 0
		
		
	func set_color(r: float, g: float, b: float):
		if sprite:
			sprite.modulate = Color(r, g, b)
	
	func ensure_sprite_setup(texture: Texture):
		if sprite == null:
			sprite = Sprite2D.new()
			sprite.texture = texture
		
		return sprite
	
	func get_quadrant(row: int, col: int) -> int:
		if col < 3 and row < 3:
			return 0
		elif col >= 3 and col < 6 and row < 3:
			return 1

		elif col >= 6 and row < 3:
			return 2
			
		elif col < 3 and row >= 3 and row < 6:
			return 3
			
		elif col >= 3 and col < 6 and row >= 3 and row < 6:
			return 4

		elif col >= 6 and row >= 3 and row < 6:
			return 5
			
		elif col < 3 and row >= 6:
			return 6
		elif col >= 3 and col < 6 and row >= 6:
			return 7

		elif col >= 6 and row >= 6:
			return 8
		else:
			return -1  # Return -1 for tiles outside of defined quadrants

	func setup_sprite(texture: Texture, region: Rect2):
		sprite = Sprite2D.new()
		sprite.texture = texture
		sprite.region_rect = region
		
		
class Grid:
	var tiles: Array = []
	var rowMates: Dictionary = {}
	var colMates: Dictionary = {}
	var groupMates: Dictionary = {}
	var openTiles: Array = []
	var name: String = ""                      
	
	func _init():
		
		for i in range(9):
			rowMates[i] = []
			colMates[i] = []
			groupMates[i] = []
		
		for row in range(9):
			var newRow: Array = []
			for col in range(9):
				var tile =  Tile.new(row, col)
				newRow.append(tile)
				
				rowMates[row].append(tile)
				colMates[col].append(tile)
				groupMates[tile.groupNumber].append(tile)
				
			tiles.append(newRow)
		
		name = "default" + str(get_save_file_count())
		
	func get_save_file_count() -> int:
		
		var dir = DirAccess.open("user://")
		
		if not dir:
			print("Error: Unable to access user directory")
			return 0

		if not dir.dir_exists("maps"):
			dir.make_dir("maps")
		
		dir.change_dir("maps")

		var file_count = 0
		dir.list_dir_begin()
		var file_name = dir.get_next()
		
		while file_name != "":
		
			if not dir.current_is_dir() and file_name.ends_with(".save"):
				file_count += 1
			file_name = dir.get_next()
	
		return file_count
	
	func load_from_saved_data(saved_data: Dictionary):
		name = saved_data.get("name", "Loaded Grid")
		tiles.clear()
		openTiles.clear()
		
		var grid_data = saved_data.get("grid", [])
		
		tiles = []
		for i in range(9):
			var row = []
			for j in range(9):
				row.append(null)
			tiles.append(row)
		
		for i in range(len(grid_data)):
			var tile_data = grid_data[i]
			var row = i / 9
			var col = i % 9
			var tile = Tile.new(row, col)
			tile.value = tile_data["value"]
			tile.trueValue = tile_data["true_value"]
			tile.open = tile_data["open"]
			tiles[row][col] = tile
			if tile.open:
				openTiles.append(tile)
			
			if tile not in rowMates[row]:
				rowMates[row].append(tile)
			if tile not in colMates[col]:
				colMates[col].append(tile)
			if tile not in groupMates[tile.groupNumber]:
				groupMates[tile.groupNumber].append(tile)
				
	
	func get_tile(row: int, col: int) -> Tile:
		return tiles[row][col]
		
	func generate() -> bool:
		var emptyTiles : Array = []
		
		for row in tiles:
			for tile in row:
				if tile.value == 0:
					emptyTiles.append(tile)
		
		var numbers = []
		for i in range(1, 10):
			numbers.append(i) 
		
		if emptyTiles.size() == 0:
			return true
			
		
		
		var tile = emptyTiles.pop_front()
		
		var badNumbers: Array = []
		
		for num in numbers:
			for mate in rowMates[tile.rowNumber]:
				if mate.value == num and num not in badNumbers:
					badNumbers.append(num)
			for mate in colMates[tile.colNumber]:
				if mate.value == num and num not in badNumbers:
					badNumbers.append(num)
			for mate in groupMates[tile.groupNumber]:
				if mate.value == num and num not in badNumbers:
					badNumbers.append(num)
					
		
		numbers.shuffle()
		
		for num in numbers:
			if num not in badNumbers:
				if check(tile, num):
					tile.value = num
					tile.trueValue = num
					if generate():
						return true
					tile.value = 0
		
		return false
			
		
	func check(tile: Tile, num: int) -> bool:
		
		var rowSafe:bool = true
		var colSafe: bool = true
		var groupSafe: bool = true
		
		for mate in rowMates[tile.rowNumber]:
			if mate.value == num and mate != tile:
				rowSafe = false
				break
				
		for mate in colMates[tile.colNumber]:
			if mate.value == num and mate != tile:
				colSafe = false
				break
				
		for mate in groupMates[tile.groupNumber]:
			if mate.value == num and mate != tile:
				groupSafe = false
				break
		
		if rowSafe and colSafe and groupSafe:
			return true
		
		return false
	
	func difficulty(num: int):
		var empty: int
		if num == 1:
			empty = 35
		elif num == 2:
			empty = 45
		elif num == 3:
			empty = 60
		
		smartRemover(empty)
		
	func smartRemover(num: int, thresh: int = 20):
		
		if num == openTiles.size():
			return
			
		var row = randi() % tiles.size()
		var col = randi() % tiles[0].size()
		var tile = tiles[row][col]
		
		while tile.value == 0:
			row = randi() % tiles.size()
			col = randi() % tiles[0].size()
			tile = tiles[row][col]
			
		
		var gMates = groupMates[tile.groupNumber]
		var rMates = rowMates[tile.rowNumber]
		var cMates = colMates[tile.colNumber]
		
		var gvalues = 0
		var rvalues = 0
		var cvalues = 0
		

		# Count the number of tiles with value 0 among group mates
		for mate in gMates:
			if mate.value == 0:
				gvalues += 1

		# Count the number of tiles with value 0 among row mates
		for mate in rMates:
			if mate.value == 0:
				rvalues += 1

		# Count the number of tiles with value 0 among column mates
		for mate in cMates:
			if mate.value == 0:
				cvalues += 1
		var combined: int = gvalues + rvalues + cvalues
		
		if combined <= thresh:
			tile.value = 0
			tile.open = true
			openTiles.append(tile)
			
		
		
		
		smartRemover(num)
		

		
		
		
		
		
