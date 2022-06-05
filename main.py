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

	mazeGrid = MazeGen.GenerateMazeGrid(20, 20)
	camera = Types.Camera(None, None, 70)

	player = Player.Player(glm.vec2(1.5, 1.5), 0, 2.5, 45)
	player.UpdateCamera(camera)

	miniMap = MiniMap.MiniMap(glm.ivec2(20, 20), glm.ivec2(200, 200), 10, 10)
	
	sprites = [
		[
			glm.vec2(2.5, 1.5),
			pygame.image.load("bennon.png")
		],
		[
			glm.vec2(5, 5),
			pygame.image.load("reid.png")
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