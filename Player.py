import pygame
import glm
import math

import Types

singleCollisionLookup = [
	glm.vec2(-0.001, -0.001),
	glm.vec2(1.001, -0.001),
	glm.vec2(-0.001, 1.001),
	glm.vec2(1.001, 1.001)
]

doubleCollisionLookup = {
	glm.ivec2(1, 0) : glm.vec2(1.001, 0),
	glm.ivec2(-1, 0) : glm.vec2(-0.001, 0),
	glm.ivec2(0, 1) : glm.vec2(0, 1.001),
	glm.ivec2(0, -1) : glm.vec2(0, -0.001),
}

class Player:
	def __init__(self, position, lookAngle, walkSpeed, turnSpeed):
		self.Position = position
		self.LookAngle = lookAngle
		self.WalkSpeed = walkSpeed
		self.TurnSpeed = turnSpeed

	def Update(self, world, windowManager):
		if windowManager.MouseCaptured:
			self.LookAngle += windowManager.MouseDelta.x

		lookVector = glm.vec2(
			math.cos(math.radians(self.LookAngle)),
			math.sin(math.radians(self.LookAngle))
		)
		rightVector = glm.vec2(lookVector.y, -lookVector.x)

		keysPressed = pygame.key.get_pressed()

		deltaTime = windowManager.DeltaTime

		moveVector = glm.vec2(0, 0)
		if keysPressed[pygame.K_w]:
			moveVector += lookVector
		if keysPressed[pygame.K_s]:
			moveVector -= lookVector
		if keysPressed[pygame.K_a]:
			moveVector += rightVector
		if keysPressed[pygame.K_d]:
			moveVector -= rightVector

		if moveVector.x != 0 or moveVector.y != 0:
			moveVector = glm.normalize(moveVector)
			
			newPosition = self.Position + moveVector * self.WalkSpeed * deltaTime

			self.Position = self._handleCollisions(newPosition, world)

	def _handleCollisions(self, newPosition, world):
		# Gather info about corners (Collision state, exact position, offset vector and corner id)
		cornerStates = [
			[world.Get(glm.ivec2(newPosition + glm.vec2(0.1, 0.1))), newPosition + glm.vec2(0.1, 0.1), glm.ivec2(1, 1), 0],
			[world.Get(glm.ivec2(newPosition + glm.vec2(-0.1, 0.1))), newPosition + glm.vec2(-0.1, 0.1), glm.ivec2(-1, 1), 1],
			[world.Get(glm.ivec2(newPosition + glm.vec2(0.1, -0.1))), newPosition + glm.vec2(0.1, -0.1), glm.ivec2(1, -1), 2],
			[world.Get(glm.ivec2(newPosition + glm.vec2(-0.1, -0.1))), newPosition + glm.vec2(-0.1, -0.1), glm.ivec2(-1, -1), 3]
		]

		# Isolate corners that are colliding
		collisions = []
		for cornerState in cornerStates:
			if cornerState[0] == 1:
				collisions.append(cornerState)

		if len(collisions) == 1:
			# Handle outer corner collision
			collision = collisions[0]

			collisionCell = glm.vec2(glm.ivec2(collision[1]))
			goal = collisionCell + singleCollisionLookup[collision[3]]

			offset = goal - collision[1]

			if offset.x < offset.y:
				newPosition.x += offset.x
			else:
				newPosition.y += offset.y

		elif len(collisions) == 2:
			# Handle flat wall collision
			collision1 = collisions[0]
			collision2 = collisions[1]

			collisionCell = glm.vec2(glm.ivec2(collision1[1]))
			moveDir = glm.normalize(newPosition - (collision1[1] + collision2[1]) / 2)
			moveDir = glm.ivec2(round(moveDir.x), round(moveDir.y))
			goal = collisionCell + doubleCollisionLookup[moveDir]

			offset = goal - collision1[1]

			if moveDir.x != 0:
				newPosition.x += offset.x
			else:
				newPosition.y += offset.y

		elif len(collisions) == 3:
			# Handle inner corner collision
			collision1 = None
			collision2 = None
			collision3 = None

			nonCorners = []
			for i in range(3):
				collision = collisions[i]

				if collision2 != None:
					nonCorners.append(collisions[i])
					continue

				v1 = collisions[(i + 1) % 3][1] - collision[1]
				v2 = collisions[(i + 2) % 3][1] - collision[1]
				
				d1 = (v1.x * v1.x + v1.y * v1.y)
				d2 = (v2.x * v2.x + v2.y * v2.y)
				
				if d1 > d2 - 0.005 and d1 < d2 + 0.005:
					collision2 = collision
					continue

				nonCorners.append(collision)

			collision1 = nonCorners[0]
			collision3 = nonCorners[1]

			collisionResponse = glm.vec2(0, 0)
			
			# First direction
			collisionCell = glm.vec2(glm.ivec2(collision1[1]))
			moveDir = glm.normalize(newPosition - (collision1[1] + collision2[1]) / 2)
			moveDir = glm.ivec2(round(moveDir.x), round(moveDir.y))
			goal = collisionCell + doubleCollisionLookup[moveDir]

			offset = goal - collision1[1]

			if moveDir.x != 0:
				collisionResponse.x += offset.x
			else:
				collisionResponse.y += offset.y

			# Second direction
			collisionCell = glm.vec2(glm.ivec2(collision3[1]))
			moveDir = glm.normalize(newPosition - (collision2[1] + collision3[1]) / 2)
			moveDir = glm.ivec2(round(moveDir.x), round(moveDir.y))
			goal = collisionCell + doubleCollisionLookup[moveDir]

			offset = goal - collision3[1]

			if moveDir.x != 0:
				collisionResponse.x += offset.x
			else:
				collisionResponse.y += offset.y

			newPosition += collisionResponse

		return newPosition

	def UpdateCamera(self, camera):
		camera.Position = self.Position
		camera.LookAngle = self.LookAngle