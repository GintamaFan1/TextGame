extends Area2D

var vacuume_direction 
var position_x_growth = 1.1007
var scale_growth = 1.1
var entered_body = []
# Called when the node enters the scene tree for the first time.
func _ready():
	$Timer.start()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	for node in entered_body:
		if node:
			node.speed = 0
		
		var distance = (position - node.position)
	
		if distance.y < 0:
			node.position -= Vector2(0, 50) * delta
		else:
			node.position += Vector2(0, 50) * delta
		
		if distance.x < 0:
			node.position -= Vector2(50,0) * delta
		else:
			node.position += Vector2(50,0) * delta
	
	
	


func _on_timer_timeout():
	var max_scale = 750.0
	if $MeshInstance2D.scale.x <= max_scale: 
		$MeshInstance2D.position *= Vector2(position_x_growth, 0)
		$MeshInstance2D.scale *= scale_growth
		
		$CollisionPolygon2D.position *= Vector2(position_x_growth, 0)
		$CollisionPolygon2D.scale *= scale_growth


func _on_body_entered(body):
	
	if body.name != "Character":
		
		entered_body.append(body)
	

		

func _on_body_exited(body):
	if body.name != "Character":
		body.speed = body.original_speed
	entered_body.erase(body)



