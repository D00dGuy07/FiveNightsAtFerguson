import pygame
import glm

KeyDown = 0
KeyPressed = 1
KeyUp = 2
KeyDefault = 3

# Should be a singleton object
class WindowManager:
	def __init__(self, screenSize, frameRate):
		self.ScreenSize = screenSize
		self.FrameRate = frameRate

		self.Surface = pygame.display.set_mode((self.ScreenSize.x, self.ScreenSize.y), pygame.RESIZABLE)
		self.Clock = pygame.time.Clock()
		self.DeltaTime = 0

		self.ShouldClose = False
		self.MouseCaptured = True
		pygame.event.set_grab(True)
		pygame.mouse.set_visible(False)

		self.KeyStates = {}

		self.MouseDelta = glm.ivec2(0, 0)

		self.FadeColor = (0, 0, 0)
		self.FadeAlpha = 0
		self.FadeVisible = 0
		self.FadeTime = 1

	def Update(self):
		self.MouseDelta = glm.ivec2(0, 0)

		# Update single "tick" key states
		for key in self.KeyStates.keys():
			if self.KeyStates[key] == KeyDown:
				self.KeyStates[key] = KeyPressed
			elif self.KeyStates[key] == KeyUp:
				self.KeyStates[key] = KeyDefault

		# Respond to all events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.ShouldClose = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.MouseCaptured = not self.MouseCaptured
					pygame.event.set_grab(self.MouseCaptured)
					pygame.mouse.set_visible(not self.MouseCaptured)

				if not self.KeyStates.get(event.key, KeyDefault) == KeyPressed:
					self.KeyStates[event.key] = KeyDown
			elif event.type == pygame.KEYUP:
				self.KeyStates[event.key] = KeyUp
			elif event.type == pygame.MOUSEMOTION:
				self.MouseDelta = glm.ivec2(event.rel[0], event.rel[1])
			elif event.type == pygame.VIDEORESIZE:
				self.ScreenSize = glm.ivec2(event.w, event.h)
				self.Surface = pygame.display.set_mode((self.ScreenSize.x, self.ScreenSize.y), pygame.RESIZABLE)

		# Capture cursor if necessary
		if self.MouseCaptured:
			pygame.mouse.set_pos((self.ScreenSize.x / 2, self.ScreenSize.y / 2))

		return self.ShouldClose

	def FinishFrame(self):
		self.DeltaTime = self.Clock.tick(self.FrameRate) / 1000 # Returns deltatime

		# Handle fade
		self.FadeAlpha = min(max((self.FadeAlpha + (255 if self.FadeVisible else -255) / self.FadeTime * self.DeltaTime), 0), 255)
		fadeSurface = pygame.Surface((self.ScreenSize.x, self.ScreenSize.y))
		fadeSurface.set_alpha(self.FadeAlpha)
		fadeSurface.fill(self.FadeColor)
		self.Surface.blit(fadeSurface, (0, 0))

		pygame.display.flip()

	def GetKeyState(self, key):
		return self.KeyStates.get(key, KeyDefault)

	def FadeIn(self, time, color):
		self.FadeColor = color
		self.FadeTime = time
		self.FadeVisible = True

	def FadeOut(self, time):
		self.FadeTime = time
		self.FadeVisible = False
	