import pygame
import glm

import ResourceManager
import TextRenderer
import WindowManager

class Grass:
	def __init__(self, position):
		self.Position = position
		self.IsHeld = False
		self.IsPlaced = False

		self.CanPickup = False

		grassImageRes = glm.ivec2(ResourceManager.GrassImage.get_width(), ResourceManager.GrassImage.get_height())
		if grassImageRes.x > grassImageRes.y:
			self._iconSize = glm.ivec2(100, round(100 * (grassImageRes.y / grassImageRes.x)))
		else:
			self._iconSize = glm.ivec2(round(100 * (grassImageRes.x / grassImageRes.y)), 100)

	def Update(self, player, windowManager):
		if not self.IsHeld:
			distToPlayer = glm.distance(self.Position, player.Position)
			self.CanPickup = distToPlayer < 1

			if self.CanPickup and windowManager.GetKeyState(pygame.K_e) == WindowManager.KeyDown:
				self.IsPlaced = False
				self.IsHeld = True
				self.CanPickup = False

		elif windowManager.GetKeyState(pygame.K_e) == WindowManager.KeyDown:
			self.IsHeld = False
			self.Position = player.Position
			self.IsPlaced = True

	def SpriteRender(self, sprites):
		if not self.IsHeld:
			sprites.append([
				self.Position,
				ResourceManager.GrassImage
			])

	def Render(self, windowManager):
		if self.IsHeld:
			iconSurface = pygame.transform.scale(ResourceManager.GrassImage, (self._iconSize.x, self._iconSize.y))
			windowManager.Surface.blit(iconSurface, (5, windowManager.ScreenSize.y - self._iconSize.y - 5))

		if self.CanPickup:
			TextRenderer.RenderText(
				"E", 
				glm.vec2(windowManager.ScreenSize) * glm.vec2(0.5, 0.6), 64, 
				(255, 255, 255), windowManager.Surface
			)