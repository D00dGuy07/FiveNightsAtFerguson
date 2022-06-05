import pygame
import glm
import math

import MazeGen
import MiniMap
import WorldLogic
import WindowManager
import Player
import Types

def main():

	# Initialize pygame
	pygame.init()

	windowManager = WindowManager.WindowManager(glm.ivec2(1080, 720), 60)

	mazeSize = glm.ivec2(5, 5)

	mazeData = MazeGen.GenerateMazeGrid(mazeSize)
	mazeGrid = mazeData.Grid

	offsets = [
		[glm.ivec2( 1,  0), 0],
		[glm.ivec2( 0,  1), 90],
		[glm.ivec2(-1,  0), 180],
		[glm.ivec2( 0, -1), 270]
	]
	pickedOffset = None
	for offset in offsets:
		if mazeGrid.Get(mazeData.StartPos + offset[0]) == 0:
			pickedOffset = offset
			break

	player = Player.Player(glm.vec2(mazeData.StartPos) + glm.vec2(0.5, 0.5) + glm.vec2(pickedOffset[0]), pickedOffset[1], 2.5)

	camera = Types.Camera(None, None, 70)

	miniMap = MiniMap.MiniMap(mazeSize, glm.ivec2(200, 200), 10, 10)
	
	endPos = WorldLogic.FindEndPos(mazeGrid, mazeData.StartPos)
	print(endPos)

	sprites = [
		[
			glm.vec2(mazeData.StartPos) + glm.vec2(0.5, 0.5),
			pygame.image.load("grass.png")
		],
		[
			glm.vec2(endPos) + glm.vec2(0.5, 0.5),
			pygame.image.load("exit.png")
		]
	]

	while not windowManager.ShouldClose:
		# Poll events
		windowManager.Update()

		# Game logic
		player.Update(mazeGrid, windowManager)
		player.UpdateCamera(camera)

		miniMap.Update(camera, mazeGrid)

		# Render
		windowManager.Surface.fill((0, 0, 0))
		WorldLogic.RenderWorld(windowManager.Surface, mazeGrid, sprites, camera)

		miniMap.Render(camera)
		mapPosition = windowManager.ScreenSize - miniMap.WindowResolution - glm.ivec2(5, 5)
		windowManager.Surface.blit(miniMap.MapWindow, (mapPosition.x, mapPosition.y))

		windowManager.FinishFrame()

if __name__ == "__main__":
	main()