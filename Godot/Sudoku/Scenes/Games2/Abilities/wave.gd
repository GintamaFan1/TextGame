extends Area2D

var vacuume_direction 
var position_x_growth = 1.1001
var scale_growth = 1.1
var entered_body = []
@export var pull_strength: float = 150.0
@export var max_pull_distance: float = 1200.0
# Called when the node enters the scene tree for the first time.
func _ready():
	$Timer.start()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	for node in entered_body:
		if node:
			
			var distance_to_character = global_position - node.global_position
			var distance = distance_to_character.length()
	
			
			if distance <= max_pull_distance:
				var pull_factor = 1 - (distance / max_pull_distance)
				var pull_force = distance_to_character.normalized() * pull_strength * pull_factor
				node.position -= pull_force * delta
	
func _on_timer_timeout():
	var max_scale = 750.0
	if $MeshInstance2D.scale.x <= max_scale: 
		$MeshInstance2D.position *= Vector2(position_x_growth, 0)
		$MeshInstance2D.scale *= scale_growth
		
		$CollisionPolygon2D.position *= Vector2(position_x_growth, 0)
		$CollisionPolygon2D.scale *= scale_growth


func _on_body_entered(body):
	
	if body.name != "Character":
		body.slow()
		entered_body.append(body)
	

		

func _on_body_exited(body):
	if body.name != "Character":
		body.unslow()
		entered_body.erase(body)
