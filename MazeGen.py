import glm
import random

import Types

def GenerateMazeGrid(width, height):
	# Prefill state lists
	grid = Types.Grid2D(width * 2 + 1, height * 2 + 1, fill=False)
	for y in range(grid.Height):
		for x in range(grid.Width):
			if (x == 0 or x == grid.Width - 1 or y == 0 or y == grid.Height - 1):
				grid.Buffer.append(1)
			elif x % 2 == 1 and y % 2 == 1:
				grid.Buffer.append(0)
			else:
				grid.Buffer.append(1)

	visitedState = Types.Grid2D(width, height, False)

	# Generate maze
	#cellStack = [glm.ivec2(random.randint(0, width - 1), random.randint(0, height - 1))]
	cellStack = [glm.ivec2(0, 0)]
	visitedState.Set(cellStack[0], True)
	while len(cellStack) > 0:
		currentCell = cellStack.pop()
		# Select neighbor
		neighborCoords = [
			currentCell + glm.ivec2(1, 0),
			currentCell + glm.ivec2(0, 1),
			currentCell + glm.ivec2(-1, 0),
			currentCell + glm.ivec2(0, -1),
		]
		
		availableNeighbors = []
		for neighbor in neighborCoords:
			if (neighbor.x > -1 and neighbor.x < width and
			   neighbor.y > -1 and neighbor.y < height):
				if not visitedState.Get(neighbor):
					availableNeighbors.append(neighbor)

		# Chose next position or backtrack if unable
		if len(availableNeighbors) > 0:
			cellStack.append(currentCell)
			nextCell = random.choice(availableNeighbors)

			# Remove wall
			cellPosition = (currentCell * 2) + glm.ivec2(1, 1)
			wallPosition = cellPosition + (nextCell - currentCell)
			grid.Set(wallPosition, 0)
			
			visitedState.Set(nextCell, True)
			cellStack.append(nextCell)

	return grid