import pygame
import glm
import math

import Types

def CastRay(grid, rayStart, rayDirection, maxDistance=100):
	# Calculate initial values and state
	rayStepSize = glm.vec2(
		0 if rayDirection.x == 0 else math.sqrt(1 + (rayDirection.y / rayDirection.x) * (rayDirection.y / rayDirection.x)),
		0 if rayDirection.y == 0 else math.sqrt(1 + (rayDirection.x / rayDirection.y) * (rayDirection.x / rayDirection.y))
	)

	currentCell = glm.ivec2(rayStart.x, rayStart.y) # Truncate to get tile
	rayLength = glm.vec2(0, 0)

	# Calculate step direction and manually align with grid
	step = glm.ivec2()

	if rayDirection.x < 0:
		step.x = -1
		rayLength.x = (rayStart.x - float(currentCell.x)) * rayStepSize.x
	else:
		step.x = 1
		rayLength.x = (float(currentCell.x + 1) - rayStart.x) * rayStepSize.x

	if rayDirection.y < 0:
		step.y = -1
		rayLength.y = (rayStart.y - float(currentCell.y)) * rayStepSize.y
	else:
		step.y = 1
		rayLength.y = (float(currentCell.y + 1) - rayStart.y) * rayStepSize.y

	tileFound = False
	distance = 0
	while not tileFound and distance < maxDistance:
		# Walk
		if rayLength.x < rayLength.y:
			currentCell.x += step.x
			distance = rayLength.x
			rayLength.x += rayStepSize.x
		else:
			currentCell.y += step.y
			distance = rayLength.y
			rayLength.y += rayStepSize.y

		if currentCell.x >= 0 and currentCell.x < grid.Width and currentCell.y >= 0 and currentCell.y < grid.Height:
			if (grid.Get(currentCell) == 1):
				tileFound = True

	if tileFound:
		return Types.RayCastResult(True, rayStart + rayDirection * distance, distance)
	return Types.RayCastResult(False, None, None)

def RenderWorld(surface, worldData, camera):
	screenSize = glm.ivec2(surface.get_width(), surface.get_height())

	for x in range(screenSize.x):
		rayAngle = (camera.LookAngle - camera.FOV / 2) + camera.FOV * (x / (screenSize.x - 1))
		rayResult = CastRay(worldData, camera.Position, glm.vec2(
			math.cos(math.radians(rayAngle)),
			math.sin(math.radians(rayAngle))
		))

		if rayResult.DidHitTile:
			adjustedDistance = max(rayResult.Distance * math.cos(math.radians(camera.LookAngle - rayAngle)), 1)
			wallHeight = max(min(screenSize.y / adjustedDistance, screenSize.y), 0)
			if wallHeight > 0:
				pygame.draw.rect(surface, (0, 0, max(255 - rayResult.Distance * 10, 0)), pygame.Rect(
					x, screenSize.y / 2 - wallHeight / 2,
					1, wallHeight
				))