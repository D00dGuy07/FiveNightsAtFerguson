import glm
import math

def AStarReconstructPath(cameFrom, current):
	totalPath = [current]
	while current in cameFrom.keys():
		current = cameFrom[current]
		totalPath.append(current)
	totalPath.reverse()
	return totalPath

def Manhattan(p1, p2):
	return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def AStarHeuristic(node, endPos):
	return Manhattan(node, endPos)


def AStar(grid, startPos, endPos):
	openSet = [startPos]
	
	cameFrom = {}

	gScore = {}
	gScore[startPos] = 0

	fScore = {}
	fScore[startPos] = AStarHeuristic(startPos, endPos)

	while len(openSet) > 0:
		current = openSet[0]
		for node in openSet:
			if fScore.get(node, math.inf) < fScore.get(current, math.inf):
				current = node

		openSet.remove(current)
		
		if current == endPos:
			return AStarReconstructPath(cameFrom, current)

		neighbors = [
			current + glm.ivec2( 0, -1),
			current + glm.ivec2( 1,  0),
			current + glm.ivec2( 0,  1),
			current + glm.ivec2(-1,  0)
		]

		for neighbor in neighbors:
			if (neighbor.x < 0 or neighbor.x >= grid.Width or 
				neighbor.y < 0 or neighbor.y >= grid.Height or 
				grid.Get(neighbor) == 1):
				continue
			
			tentativeGScore = gScore.get(current, math.inf) + Manhattan(current, neighbor)
			if tentativeGScore < gScore.get(neighbor, math.inf):
				cameFrom[neighbor] = current
				gScore[neighbor] = tentativeGScore
				fScore[neighbor] = tentativeGScore + AStarHeuristic(neighbor, endPos)
				if neighbor not in openSet:
					openSet.append(neighbor)

	return []