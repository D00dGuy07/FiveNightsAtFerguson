import pygame
import glm
import math

import Types

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

			cornerStates = [
				world.Get(glm.ivec2(newPosition + glm.vec2(0.1, 0.1))),
				world.Get(glm.ivec2(newPosition + glm.vec2(-0.1, 0.1))),
				world.Get(glm.ivec2(newPosition + glm.vec2(0.1, -0.1))),
				world.Get(glm.ivec2(newPosition + glm.vec2(-0.1, -0.1))),
			]

			totalCollisions = 0
			for cornerState in cornerStates:
				totalCollisions += cornerState
			print(totalCollisions)

			self.Position = newPosition


	def UpdateCamera(self, camera):
		camera.Position = self.Position
		camera.LookAngle = self.LookAngle