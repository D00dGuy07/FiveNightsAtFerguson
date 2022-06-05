import pygame
import glm
import math

import Types

def drawWallSection(data, surface):
	# Data = [color, x, y, height]
	pygame.draw.rect(surface, data[0], pygame.Rect(
		data[1], data[2],
		1, data[3]
	))

def drawSprite(data, surface):
	surface.blit(
		data[0],
		(data[1], data[2])
	)

def renderQueueSort(value):
	return value[0]

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
		return Types.RayCastResult(True, rayStart + rayDirection * distance, currentCell, distance)
	return Types.RayCastResult(False, None, None, None)

def RenderWorld(surface, worldData, sprites, camera):
	screenSize = glm.ivec2(surface.get_width(), surface.get_height())

	renderQueue = []

	for sprite in sprites:
		if screenSize.x == 1 or camera.FOV == 0:
			break

		directionVector = sprite[0] - camera.Position

		a = round(math.degrees(math.atan2(directionVector.y, directionVector.x)))
		distance = glm.length(directionVector)

		rayResult = CastRay(worldData, camera.Position, glm.vec2(
			math.cos(math.radians(a)),
			math.sin(math.radians(a))
		))
		distanceDifference = distance - rayResult.Distance
		if distanceDifference > 1:
			continue # Don't render if there's a wall blocking it

		adjustedDistance = distance * math.cos(math.radians(camera.LookAngle - a))
		if adjustedDistance == 0: continue

		l = camera.LookAngle - 360 if camera.LookAngle > 180 else camera.LookAngle
		f = camera.FOV
		s = screenSize.x

		x = (2*a*s - 2*a - 2*l*s + 2*l + s*f - f) / (2*f) # x screen coordinate

		height = screenSize.y / adjustedDistance / 2
		width = height * (sprite[1].get_width() / sprite[1].get_height())

		if width < 1 or height < 1 or adjustedDistance < 0.1: continue
		surfaceCopy = pygame.transform.scale(sprite[1], (width, height))

		renderQueue.append([
			adjustedDistance,
			drawSprite,
			[
				surfaceCopy,
				x - width / 2, screenSize.y / 2 - height/ 2
			]
		])

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
				pos = rayResult.CollisionPoint

				color = None
				distanceFog = max(1 - pow(rayResult.Distance, 1.3) / 5, 0)
				if round(pos.x * 2) % 2 == 0 and round(pos.y * 2) % 2 == 0:
					color = glm.vec3(235, 161, 52) * distanceFog
				else:
					color = glm.vec3(255, 255, 255) * distanceFog

				renderQueue.append([
					adjustedDistance,
					drawWallSection,
					[
						(color.x, color.y, color.z),
						x, screenSize.y / 2 - wallHeight / 2,
						wallHeight
					]
				])

	renderQueue.sort(reverse=True, key=renderQueueSort)

	for renderTask in renderQueue:
		renderTask[1](renderTask[2], surface)
	
def endPosSort(value):
	return value[1]

def FindEndPos(grid, startPos):
	offsets = [
		glm.ivec2( 1,  0),
		glm.ivec2( 0,  1),
		glm.ivec2(-1,  0),
		glm.ivec2( 0, -1)
	]

	lessSuitablePositions = []
	suitablePositions = []
	for y in range(grid.Height):
		for x in range(grid.Width):
			coord = glm.ivec2(x, y)
			if grid.Get(coord) == 1:
				continue

			coordData = [coord, glm.distance2(glm.vec2(startPos), glm.vec2(coord))]
			lessSuitablePositions.append(coordData)

			emptyCount = 0
			for offset in offsets:
				emptyCount += int(grid.Get(coord + offset) == 0)

			if emptyCount == 1:
				suitablePositions.append(coordData)

	if len(suitablePositions) == 0:
		lessSuitablePositions.sort(reverse=True, key=endPosSort)
		return lessSuitablePositions[0][0]

	suitablePositions.sort(reverse=True, key=endPosSort)
	return suitablePositions[0][0]