extends Area2D
signal game_won(result)

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(_delta):
	if Sucker.train_health <= 0:
		game_won.emit(false)


func _on_body_entered(body):
	if "enemy" in body.name.to_lower():
		Sucker.train_health -= Sucker.ENEMY_DAMAGE
		body.explode()
	
	if body.name == "Character":
		game_won.emit(true)
	
	
	
