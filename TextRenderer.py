import pygame

import ResourceManager

def RenderText(text, position, size, color, surface):
	font = ResourceManager.Fonts.get(size)

	if font != None:
		textImage = font.render(text, True, color)
		width = textImage.get_width()
		height = textImage.get_height()

		surface.blit(textImage, (position.x - width / 2, position.y - height / 2))