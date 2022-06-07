import pygame
import glm

import MazeGen
import MiniMap
import WorldLogic
import Player
import Types
import Reid

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
		self.GrassPos = WorldLogic.FindRandomEmpty(self.MazeGrid)

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
		self.Camera = Types.Camera(None, None, 70)
		self.MiniMap = MiniMap.MiniMap(mazeSize, glm.ivec2(200, 200), 10, 10)

		self.Reid = Reid.Reid(glm.vec2(WorldLogic.FindFirstAdjacentEmpty(self.MazeGrid, self.StartPos)) + glm.vec2(0.5, 0.5), 1)
		self.Reid.MoveTo(glm.vec2(self.EndPos))

		# Sprite rendering data
		self.Sprites = [
			[
				self.Reid.Position,
				ResourceManager.ReidImage
			],
			[
				glm.vec2(self.GrassPos) + glm.vec2(0.5, 0.5),
				ResourceManager.GrassImage
			],
			[
				glm.vec2(self.EndPos) + glm.vec2(0.5, 0.5),
				ResourceManager.ExitImage
			]
		]

	def Update(self):
		self.Player.Update(self.MazeGrid, self.WindowManager)
		self.Player.UpdateCamera(self.Camera)
		self.MiniMap.Update(self.Camera, self.MazeGrid)

		self.Reid.Update(self.MazeGrid, self.WindowManager.DeltaTime)
		self.Reid.MoveTo(self.Player.Position)
		self.Sprites[0][0] = self.Reid.Position

	def Render(self):
		self.WindowManager.Surface.fill((0, 0, 0))
		WorldLogic.RenderWorld(self.WindowManager.Surface, self.MazeGrid, self.Sprites, self.Camera)

		self.MiniMap.Render(self.Camera)
		mapPosition = self.WindowManager.ScreenSize - self.MiniMap.WindowResolution - glm.ivec2(5, 5)
		self.WindowManager.Surface.blit(self.MiniMap.MapWindow, (mapPosition.x, mapPosition.y))
