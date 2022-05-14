import pygame
import glm
import math

import MazeGen
import Types

def drawGrid(surface, color, grid, cellWidth, cellHeight):
	for y in range(grid.Height):
		for x in range(grid.Width):
			if grid.Get(glm.ivec2(x, y)) == 1:
				pygame.draw.rect(surface, color, pygame.Rect(x * cellWidth, y * cellHeight, cellWidth, cellHeight))

def castRay(grid, rayStart, rayDirection, maxDistance=100):
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

def main():
	width = 20
	height = 20

	cellWidth = 10
	cellHeight = 10

	frameRate = 30

	FOV = 70
	playerSpeed = 2.5
	
	mazeGrid = MazeGen.GenerateMazeGrid(width, height)

	# Initialize pygame
	pygame.init()

	screenSize = glm.ivec2(1080, 720)
	surface = pygame.display.set_mode((screenSize.x, screenSize.y))

	# Game loop
	clock = pygame.time.Clock()
	deltaTime = 0

	playerPos = glm.vec2(1.5, 1.5)
	playerAngle = 0

	mouseGrabbed = False
	running = True
	while running:
		# Poll events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					mouseGrabbed = not mouseGrabbed
					pygame.event.set_grab(mouseGrabbed)
					pygame.mouse.set_visible(not mouseGrabbed)
			elif event.type == pygame.MOUSEMOTION and mouseGrabbed:
				playerAngle += event.rel[0] / 4

		if mouseGrabbed:
			pygame.mouse.set_pos((screenSize.x / 2, screenSize.y / 2))

		# Game logic
		lookVector = glm.vec2(
			math.cos(math.radians(playerAngle)),
			math.sin(math.radians(playerAngle))
		)
		rightVector = glm.vec2(lookVector.y, -lookVector.x)

		keysPressed = pygame.key.get_pressed()

		# WASD Control
		if keysPressed[pygame.K_w]:
			playerPos += lookVector * playerSpeed * deltaTime
		if keysPressed[pygame.K_s]:
			playerPos -= lookVector * playerSpeed * deltaTime
		if keysPressed[pygame.K_a]:
			playerPos += rightVector * playerSpeed * deltaTime
		if keysPressed[pygame.K_d]:
			playerPos -= rightVector * playerSpeed * deltaTime

		# Arrow key control control
		if keysPressed[pygame.K_LEFT]:
			playerAngle -= 45 * deltaTime
		if keysPressed[pygame.K_RIGHT]:
			playerAngle += 45 * deltaTime
		if keysPressed[pygame.K_UP]:
			playerPos += lookVector * playerSpeed * deltaTime
		if keysPressed[pygame.K_DOWN]:
			playerPos -= lookVector * playerSpeed * deltaTime

		
		# Render
		surface.fill((0, 0, 0))
		#drawGrid(surface, (0, 0, 255), mazeGrid, cellWidth, cellHeight)

		for x in range(screenSize.x):
			angle = (playerAngle - FOV / 2) + FOV * (x / (screenSize.x - 1))
			rayResult = castRay(mazeGrid, playerPos, glm.vec2(
				math.cos(math.radians(angle)),
				math.sin(math.radians(angle))
			))

			if rayResult.DidHitTile:
				adjustedDistance = max(rayResult.Distance * math.cos(math.radians(playerAngle - angle)), 1)
				height = max(min(screenSize.y / adjustedDistance, screenSize.y), 0)
				if height > 0:
					pygame.draw.rect(surface, (0, 0, max(255 - rayResult.Distance * 10, 0)), pygame.Rect(
						x, screenSize.y / 2 - height / 2,
						1, height
					))
		
		pygame.display.flip()

		# Limit framerate
		deltaTime = clock.tick(frameRate) / 1000 # Returns deltatime

if __name__ == "__main__":
	main()