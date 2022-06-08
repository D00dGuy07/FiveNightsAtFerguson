import pygame
pygame.init()

import glm

import WindowManager
import SceneManager
import TextRenderer

PlayerDied = 1
PlayerCaught = 2
PlayerEscaped = 3
ExitGame = 4

def RunLevel(sceneManager, windowManager):
	windowManager.FadeAlpha = 255
	windowManager.FadeOut(5)

	while not windowManager.ShouldClose:
		# Update
		windowManager.Update()
		sceneManager.Update()

		if sceneManager.Player.Dead:
			return PlayerDied

		if sceneManager.Exit.PlayerExited:
			if sceneManager.Exit.PlayerCaught:
				return PlayerCaught
			else:
				return PlayerEscaped

		# Render
		sceneManager.Render()
		windowManager.FinishFrame()

	return ExitGame

def RunLevelAndResults(windowManager, size):
	sceneManager = SceneManager.SceneManager(size, windowManager)
	result = RunLevel(sceneManager, windowManager)
	windowManager.FadeIn(1, (0, 0, 0))
	timer = 1
	while timer > 0 and not windowManager.ShouldClose:
		windowManager.Update()
		windowManager.FinishFrame()
		timer -= windowManager.DeltaTime
	windowManager.Surface.fill((0, 0, 0))
	windowManager.FadeOut(1)
	windowManager.FadeAlpha = 0

	if (not HandleLevelResult(windowManager, result)):
		return False
	return True

def DisplayTimedText(windowManager, text, color, time):
	timer = time + 1

	while timer - 1 > 0 and not windowManager.ShouldClose:
		windowManager.Update()
		TextRenderer.RenderText(text, windowManager.ScreenSize / 2, 38, color, windowManager.Surface)
		windowManager.FinishFrame()
		timer -= windowManager.DeltaTime

	windowManager.FadeIn(1, (0, 0, 0))

	while timer > 0 and not windowManager.ShouldClose:
		windowManager.Update()
		TextRenderer.RenderText(text, windowManager.ScreenSize / 2, 38, color, windowManager.Surface)
		windowManager.FinishFrame()
		timer -= windowManager.DeltaTime

	windowManager.FadeOut(1)
	windowManager.FadeAlpha = 0

def StartSequence(windowManager):
	DisplayTimedText(windowManager, "You're trapped in Reid's lair...", (255, 255, 255), 5)
	DisplayTimedText(windowManager, "Reid is guarding the exit...", (255, 255, 255), 5)
	DisplayTimedText(windowManager, "lead him away with the grass...", (255, 255, 255), 5)
	DisplayTimedText(windowManager, "It's somewhere around here...", (255, 255, 255), 5)

def HandleLevelResult(windowManager, result):
	if result == PlayerDied:
		DisplayTimedText(windowManager, "You died", (255, 0, 0), 5)
		return False
	elif result == PlayerCaught:
		DisplayTimedText(windowManager, "Reid caught you escaping", (255, 0, 0), 5)
		return False
	elif result == ExitGame:
		return False
	return True

def Run():
	windowManager = WindowManager.WindowManager(glm.ivec2(1080, 720), 60)

	StartSequence(windowManager)

	# First level
	if not RunLevelAndResults(windowManager, glm.ivec2(5, 5)):
		return
	DisplayTimedText(windowManager, "Surely you didn't think you're done", (255, 255, 255), 5)
	DisplayTimedText(windowManager, "Did you?", (255, 255, 255), 2)

	# Second level
	if not RunLevelAndResults(windowManager, glm.ivec2(7, 7)):
		return
	DisplayTimedText(windowManager, "This is getting difficult huh?", (255, 255, 255), 5)

	# Third level
	if not RunLevelAndResults(windowManager, glm.ivec2(9, 9)):
		return
	DisplayTimedText(windowManager, "I'm surprised you've gotten this far", (255, 255, 255), 5)

	# Fourth level
	if not RunLevelAndResults(windowManager, glm.ivec2(11, 11)):
		return
	DisplayTimedText(windowManager, "You can just give up now.", (255, 255, 255), 5)

	# Fifth level
	if not RunLevelAndResults(windowManager, glm.ivec2(13, 13)):
		return
	DisplayTimedText(windowManager, "Insert text here", (255, 255, 255), 5)