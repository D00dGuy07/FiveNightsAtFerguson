import pygame
import glm

import MazeGen
import MiniMap
import WorldLogic
import Player
import Types
import Reid
import Grass
import TextRenderer
import LevelExit

import ResourceManager

class SceneManager:
	def __init__(self, mazeSize, windowManager):
		self.MazeSize = mazeSize
		self.WindowManager = windowManager

		# Generate maze
		mazeData = MazeGen.GenerateMazeGrid(self.MazeSize)
		self.MazeGrid = mazeData.Grid
		self.StartPos = mazeData.StartPos
		self.EndPos = WorldLogic.FindEndPos(self.MazeGrid, self.StartPos)
		self.Exit = LevelExit.LevelExit(self.EndPos)

		grassPos = WorldLogic.FindRandomEmpty(self.MazeGrid)
		self.Grass = Grass.Grass(glm.vec2(grassPos) + glm.vec2(0.5, 0.5),)

		# Create the player
		offsets = [
			[glm.ivec2( 1,  0), 0],
			[glm.ivec2( 0,  1), 90],
			[glm.ivec2(-1,  0), 180],
			[glm.ivec2( 0, -1), 270]
		]
		pickedOffset = None
		for offset in offsets:
			if self.MazeGrid.Get(self.StartPos + offset[0]) == 0:
				pickedOffset = offset
				break
		self.Player = Player.Player(
			glm.vec2(self.StartPos) + glm.vec2(0.5, 0.5), pickedOffset[1], 2.5)

		# Create the camera and minimap
		self.Camera = Types.Camera(None, None, 80)
		self.MiniMap = MiniMap.MiniMap(mazeSize, glm.ivec2(200, 200), 10, 10)

		self.Reid = Reid.Reid(glm.vec2(WorldLogic.FindFirstAdjacentEmpty(self.MazeGrid, self.EndPos)) + glm.vec2(0.5, 0.5), 1.5)

		# Sprite rendering data
		self.Sprites = []

	def Update(self):
		self.Player.Update(self.MazeGrid, self.WindowManager)
		self.Player.UpdateCamera(self.Camera)
		self.MiniMap.Update(self.Camera, self.MazeGrid)

		self.Reid.Update(self.MazeGrid, self.Player, self.Grass, self.WindowManager.DeltaTime)
		self.Grass.Update(self.Player, self.WindowManager)

		self.Exit.Update(self.Player, self.Reid, self.MazeGrid)

	def Render(self):
		self.WindowManager.Surface.fill((0, 0, 0))

		self.Sprites.clear()

		self.Reid.SpriteRender(self.Sprites)
		self.Grass.SpriteRender(self.Sprites)
		self.Exit.SpriteRender(self.Sprites)

		WorldLogic.RenderWorld(self.WindowManager.Surface, self.MazeGrid, self.Sprites, self.Camera)

		self.Grass.Render(self.WindowManager)

		self.MiniMap.Render(self.Camera)
		mapPosition = self.WindowManager.ScreenSize - self.MiniMap.WindowResolution - glm.ivec2(5, 5)
		self.WindowManager.Surface.blit(self.MiniMap.MapWindow, (mapPosition.x, mapPosition.y))
