import glm

class Grid2D:
	def __init__(self, width, height, default=0, fill=True):
		self.Width = width
		self.Height = height
		if fill:
			self.Buffer = [default] * width * height
		else:
			self.Buffer = []

	def Get(self, coord):
		return self.Buffer[coord.y * self.Width + coord.x]

	def Set(self, coord, value):
		self.Buffer[coord.y * self.Width + coord.x] = value

class RayCastResult:
	def __init__(self, didHitTile, collisionPoint, distance):
		self.DidHitTile = didHitTile
		self.CollisionPoint = collisionPoint
		self.Distance = distance