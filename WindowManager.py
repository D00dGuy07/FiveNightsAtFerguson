import pygame
import glm

# Should be a singleton object
class WindowManager:
	def __init__(self, screenSize, frameRate):
		self.ScreenSize = screenSize
		self.FrameRate = frameRate

		self.Surface = pygame.display.set_mode((self.ScreenSize.x, self.ScreenSize.y), pygame.RESIZABLE)
		self.Clock = pygame.time.Clock()
		self.DeltaTime = 0

		self.ShouldClose = False
		self.MouseCaptured = False

		self.MouseDelta = glm.ivec2(0, 0)

	def Update(self):
		self.MouseDelta = glm.ivec2(0, 0)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.ShouldClose = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.MouseCaptured = not self.MouseCaptured
					pygame.event.set_grab(self.MouseCaptured)
					pygame.mouse.set_visible(not self.MouseCaptured)
			elif event.type == pygame.MOUSEMOTION:
				self.MouseDelta = glm.ivec2(event.rel[0], event.rel[1])
			elif event.type == pygame.VIDEORESIZE:
				self.ScreenSize = glm.ivec2(event.w, event.h)
				self.Surface = pygame.display.set_mode((self.ScreenSize.x, self.ScreenSize.y), pygame.RESIZABLE)

		if self.MouseCaptured:
			pygame.mouse.set_pos((self.ScreenSize.x / 2, self.ScreenSize.y / 2))

		return self.ShouldClose

	def FinishFrame(self):
		pygame.display.flip()
		self.DeltaTime = self.Clock.tick(self.FrameRate) / 1000 # Returns deltatime