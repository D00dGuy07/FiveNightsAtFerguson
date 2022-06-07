import glm
import math

import Pathfinding

class Reid:
	def __init__(self, position, walkSpeed):
		self.Position = position
		self.WalkSpeed = walkSpeed

		self.TargetPosition = position
		self.Path = []
		self.ShouldRecalculatePath = False

	def MoveTo(self, location):
		self.TargetPosition = location
		self.ShouldRecalculatePath = True

	# Must have a path to call this
	def GetCheckpoint(self):
		if isinstance(self.Path[-1], glm.ivec2):
			return glm.vec2(self.Path[-1]) + glm.vec2(0.5, 0.5) # Cell coordinate (get center)
		else:
			return self.Path[-1] # Exact coordinate

	def Update(self, grid, deltaTime):
		if deltaTime <= 0:
			return

		if self.ShouldRecalculatePath:
			self.ShouldRecalculatePath = False
			self.Path = Pathfinding.AStar(grid, glm.ivec2(self.Position), glm.ivec2(self.TargetPosition))
			self.Path.append(self.TargetPosition)
			self.Path.reverse()
			self.Path.pop()

		if len(self.Path) > 0:
			checkPoint = self.GetCheckpoint()
			if glm.distance(self.Position, checkPoint) < self.WalkSpeed * deltaTime * 2:
				self.Path.pop()
				if len(self.Path) < 1:
					return
				checkPoint = self.GetCheckpoint()

			direction = glm.normalize(checkPoint - self.Position)
			self.Position += direction * self.WalkSpeed * deltaTime