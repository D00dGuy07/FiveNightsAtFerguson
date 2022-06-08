import glm
import math

import WorldLogic
import Pathfinding
import ResourceManager

class Reid:
	def __init__(self, position, walkSpeed):
		self.Position = position
		self.WalkSpeed = walkSpeed

		self.TargetPosition = position
		self.Path = []
		self.ShouldRecalculatePath = False

		self.FoundPlayer = False
		self.DistractedTimeout = 0
		self.GrassCooldown = 0

	def MoveTo(self, location):
		self.TargetPosition = location
		self.ShouldRecalculatePath = True

	# Must have a path to call this
	def _getCheckpoint(self):
		if isinstance(self.Path[-1], glm.ivec2):
			return glm.vec2(self.Path[-1]) + glm.vec2(0.5, 0.5) # Cell coordinate (get center)
		else:
			return self.Path[-1] # Exact coordinate

	def _isVisible(self, position, grid):
		directionVector = position - self.Position
		pointDistance = glm.length(directionVector)

		rayResult = WorldLogic.CastRay(grid, self.Position, glm.normalize(directionVector))
		if rayResult.Distance > pointDistance and pointDistance < 2:
			return True
		return False

	def Update(self, grid, player, grass, deltaTime):
		self.DistractedTimeout = max(self.DistractedTimeout - deltaTime, 0)
		self.GrassCooldown = max(self.GrassCooldown - deltaTime, 0)
		
		playerVector = player.Position - self.Position
		playerDistance = glm.length(playerVector)

		# Wait for the player to walk by
		if not self.FoundPlayer:
			self.FoundPlayer = self._isVisible(player.Position, grid)
			if self.FoundPlayer:
				self.DistractedTimeout = 0.5

		# He must get distracted by grass
		if grass.IsPlaced and self._isVisible(grass.Position, grid) and self.GrassCooldown == 0:
			self.MoveTo(grass.Position)
			self.DistractedTimeout = 5
			self.GrassCooldown = 10

		# Follow player while not eating grass
		if self.FoundPlayer and self.DistractedTimeout == 0:
			self.MoveTo(player.Position)

		# Last little bit of logic
		if self.DistractedTimeout == 0 and glm.distance(self.Position, player.Position) < 0.5:
			player.Dead = True

		# Follow pathfound path
		if deltaTime <= 0:
			return

		if self.ShouldRecalculatePath:
			self.ShouldRecalculatePath = False
			self.Path = Pathfinding.AStar(grid, glm.ivec2(self.Position), glm.ivec2(self.TargetPosition))
			self.Path.append(self.TargetPosition)
			self.Path.reverse()
			self.Path.pop()

		if len(self.Path) > 0:
			checkPoint = self._getCheckpoint()
			if glm.distance(self.Position, checkPoint) < self.WalkSpeed * deltaTime * 2:
				self.Path.pop()
				if len(self.Path) < 1:
					return
				checkPoint = self._getCheckpoint()

			direction = glm.normalize(checkPoint - self.Position)
			self.Position += direction * self.WalkSpeed * deltaTime

	def SpriteRender(self, sprites):
		sprites.append([
			self.Position,
			ResourceManager.ReidImage
		])