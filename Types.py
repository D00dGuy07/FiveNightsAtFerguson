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
		if coord.x >= 0 and coord.x < self.Width and coord.y >= 0 and coord.y < self.Height:
			return self.Buffer[coord.y * self.Width + coord.x]
		return 0

	def Set(self, coord, value):
		self.Buffer[coord.y * self.Width + coord.x] = value

class RayCastResult:
	def __init__(self, didHitTile, collisionPoint, distance):
		self.DidHitTile = didHitTile
		self.CollisionPoint = collisionPoint
		self.Distance = distance

class Camera:
	def __init__(self, position, lookAngle, fov):
		self.Position = position
		self.LookAngle = lookAngle
		self.FOV = fov