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

	def Update(self, windowManager):
		if windowManager.MouseCaptured:
			self.LookAngle += windowManager.MouseDelta.x

		lookVector = glm.vec2(
			math.cos(math.radians(self.LookAngle)),
			math.sin(math.radians(self.LookAngle))
		)
		rightVector = glm.vec2(lookVector.y, -lookVector.x)

		keysPressed = pygame.key.get_pressed()

		deltaTime = windowManager.DeltaTime

		# WASD Control
		if keysPressed[pygame.K_w]:
			self.Position += lookVector * self.WalkSpeed * deltaTime
		if keysPressed[pygame.K_s]:
			self.Position -= lookVector * self.WalkSpeed  * deltaTime
		if keysPressed[pygame.K_a]:
			self.Position += rightVector * self.WalkSpeed  * deltaTime
		if keysPressed[pygame.K_d]:
			self.Position -= rightVector * self.WalkSpeed  * deltaTime

		# Arrow key control control
		if keysPressed[pygame.K_LEFT]:
			self.LookAngle -= self.TurnSpeed * deltaTime
		if keysPressed[pygame.K_RIGHT]:
			self.LookAngle += self.TurnSpeed * deltaTime
		if keysPressed[pygame.K_UP]:
			self.Position += lookVector * self.WalkSpeed  * deltaTime
		if keysPressed[pygame.K_DOWN]:
			self.Position -= lookVector * self.WalkSpeed  * deltaTime

	def UpdateCamera(self, camera):
		camera.Position = self.Position
		camera.LookAngle = self.LookAngle