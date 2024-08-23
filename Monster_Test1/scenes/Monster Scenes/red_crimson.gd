extends Monsters

var using_flamethrower: bool = false


func _on_animated_sprite_2d_frame_changed() -> void:
	if $AnimatedSprite2D.animation == "attack":
		if $AnimatedSprite2D.frame == 2:
			$AnimatedSprite2D.pause()
			
			using_flamethrower = true
			await use_flamethrower()
	else:
		using_flamethrower = false
		use_flamethrower()

func use_flamethrower():
	if using_flamethrower == true:
		
		$AnimatedSprite2D2.show()
		$AnimatedSprite2D2.play("begin")
		await $AnimatedSprite2D2.animation_finished
		
		$AnimatedSprite2D2.play("middle")
		await $AnimatedSprite2D2.animation_finished
		
		$AnimatedSprite2D2.play("end")
		
	else:
		
		$AnimatedSprite2D2.hide()
		
	
	
	
		
