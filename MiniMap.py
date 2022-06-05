import pygame
import glm
import math

import WorldLogic
import Types

class MiniMap:
	def __init__(self, size, windowResolution, cellSize, mapView):
		self.MapView = mapView
		self.CellSize = cellSize
		self.GridSize = glm.ivec2(size.x * 2 + 1, size.y * 2 + 1)
		self.MapResolution = self.GridSize * self.CellSize
		self.WindowResolution = windowResolution

		#self.InternalGrid = Types.Grid2D(self.GridSize.x, self.GridSize.y, fill=True)
					
		self.MapSurface = pygame.Surface((self.MapResolution.x, self.MapResolution.y))
		self.MapWindow = pygame.Surface((self.WindowResolution.x, self.WindowResolution.y))

	def Render(self, camera):
		# self.MapSurface.fill((0, 0, 0))
		# for y in range(self.InternalGrid.Height):
		# 	for x in range(self.InternalGrid.Width):
		# 		if self.InternalGrid.Get(glm.ivec2(x, y)) == 1:
		# 			pygame.draw.rect(
		# 				self.MapSurface, (0, 255, 0), 
		# 				pygame.Rect(x * self.CellSize, y * self.CellSize, self.CellSize, self.CellSize)
		# 			)

		translateCoordinates = (glm.vec2(self.GridSize) / 2 - camera.Position) * self.CellSize
		smallerSize = self.WindowResolution.x if self.WindowResolution.x < self.WindowResolution.y else self.WindowResolution.y

		intermediateSurface = pygame.Surface((self.MapResolution.x, self.MapResolution.y))
		intermediateSurface.blit(self.MapSurface, (translateCoordinates.x, translateCoordinates.y))
		intermediateSurface = pygame.transform.rotozoom(intermediateSurface, camera.LookAngle + 90, smallerSize / (self.CellSize * self.MapView))
		
		width = intermediateSurface.get_width()
		height = intermediateSurface.get_height()

		self.MapWindow.blit(intermediateSurface, (self.WindowResolution.x / 2 - width / 2, self.WindowResolution.y / 2 - height / 2))

	def Update(self, camera, worldData):
		rayCount = round(camera.FOV / 10)
		for x in range(rayCount):
			rayAngle = (camera.LookAngle - camera.FOV / 2) + camera.FOV * (x / (rayCount - 1)) 
			rayResult = WorldLogic.CastRay(worldData, camera.Position, glm.vec2(
				math.cos(math.radians(rayAngle)),
				math.sin(math.radians(rayAngle))
			), 3.449)

			if rayResult.DidHitTile:
				#self.InternalGrid.Set(rayResult.CellCoordinates, 1)
				pos = rayResult.CollisionPoint * self.CellSize
				pygame.draw.rect(self.MapSurface, (0, 255, 0), pygame.Rect(pos.x, pos.y, 1, 1))