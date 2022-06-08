import glm

import ResourceManager

class LevelExit:
	def __init__(self, cellPosition):
		self.CellPosition = cellPosition
		self.ExactPosition = glm.vec2(cellPosition) + glm.vec2(0.5, 0.5)

		self.PlayerExited = False
		self.PlayerCaught = False

	def Update(self, player, reid, grid):
		playerDist = glm.distance(self.ExactPosition, player.Position)

		if playerDist < 0.5:
			# Kinda dirty using reid's personal function but oh well, it's useful
			if reid._isVisible(player.Position, grid):
				self.PlayerExited = True
				self.PlayerCaught = True
			else:
				self.PlayerExited = True

	def SpriteRender(self, sprites):
		sprites.append([
			self.ExactPosition,
			ResourceManager.ExitImage
		])