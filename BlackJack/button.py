import pygame
from pygame.locals import *

state = 0 

#button class
class Button():
	def __init__(self, x, y, image, image_tuto, scale, state_image):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image_tuto = pygame.transform.scale(image_tuto, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.state_image = state_image 

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		image = self.image if state != self.state_image else self.image_tuto
		CursorOnButton = False

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			CursorOnButton = True
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		copy = image.copy()

		if CursorOnButton : 
			copy.fill((255, 255, 255, 160), special_flags=BLEND_RGBA_MULT)
		else : 
			copy.fill((255, 255, 255, 255), special_flags=BLEND_RGBA_MULT)
		
		#draw button on screen
		surface.blit(copy, (self.rect.x, self.rect.y))

		return action