extends Area2D

var vacuume_direction 
var position_x_growth = 1.1007
var scale_growth = 1.1

# Called when the node enters the scene tree for the first time.
func _ready():
	$Timer.start()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	
	modulate = Color(.9, .3, .2, 1)
	


func _on_timer_timeout():
	var max_scale = 750.0
	if $MeshInstance2D.scale.x <= max_scale: 
		$MeshInstance2D.position *= Vector2(position_x_growth, 0)
		$MeshInstance2D.scale *= scale_growth
		
		$CollisionPolygon2D.position *= Vector2(position_x_growth, 0)
		$CollisionPolygon2D.scale *= scale_growth


func _on_body_entered(body):
	var difference = (position - body.position).normalized()
	body.position += difference
