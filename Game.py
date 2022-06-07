import pygame
import glm

import WindowManager
import SceneManager

def Run():
	pygame.init()

	windowManager = WindowManager.WindowManager(glm.ivec2(1080, 720), 60)
	sceneManager = SceneManager.SceneManager(glm.ivec2(5, 5), windowManager)

	while not windowManager.ShouldClose:
		# Update
		windowManager.Update()
		sceneManager.Update()

		# Render
		sceneManager.Render()
		windowManager.FinishFrame()

