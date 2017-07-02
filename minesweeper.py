#!/usr/bin/python3

"""
Minesweeper game made with Python3 and Pygame

Author: Ricardo Henrique Remes de Lima <https://www.github.com/rhrlima>

Source: https://www.youtube.com/user/shiffman
"""

import pygame
from pygame.locals import *

import random


NUMBER_OF_BOMBS = 10
GRID_SIZE = 20
WINDOW_W = 400
WINDOW_H = 400


BLACK 		= (0, 0, 0)
WHITE 		= (255, 255, 255)
GREY		= (230, 230, 230)
DARK_GREY	= (100, 100, 100)
BLUE		= (0, 162, 232)
DARK_BLUE 	= (0, 64, 128)
GREEN 		= (34, 177, 76)
RED 		= (237, 28, 36)
DARK_RED 	= (128, 0, 0)
PURPLE 		= (163, 73, 164)
DARK_PURPLE = (128, 0, 128)


class Cell:

	def __init__(self, i, j, w):
		self.i = i
		self.j = j
		self.x = i * w
		self.y = j * w
		self.w = w
		self.revealed = False
		self.bomb = False
		self.maybe = False
		self.exploded = False
		self.deactivated = False
		self.number_bombs = 0

	def reveal(self):
		self.revealed = True

	def draw(self, surface, font):
		pygame.draw.rect(surface, BLACK, Rect([self.x, self.y], [self.w, self.w]), 1)
		if self.revealed:
			if self.bomb:
				if self.exploded:
					pygame.draw.rect(surface, RED, Rect([self.x+1, self.y+1], [self.w-2, self.w-2]))
				elif self.deactivated:
					pygame.draw.rect(surface, GREEN, Rect([self.x+1, self.y+1], [self.w-2, self.w-2]))
				pygame.draw.circle(surface, BLACK, ( self.x+self.w//2, self.y+self.w//2 ), self.w//2-2, 0)
			else:
				pygame.draw.rect(surface, GREY, Rect([self.x+1, self.y+1], [self.w-2, self.w-2]))
				if self.number_bombs > 0:
					color = None
					if self.number_bombs == 1:
						color = BLUE
					elif self.number_bombs == 2:
						color = GREEN
					elif self.number_bombs == 3:
						color = RED
					elif self.number_bombs == 4:
						color = DARK_BLUE
					elif self.number_bombs == 5:
						color = DARK_RED
					elif self.number_bombs == 6:
						color = PURPLE
					elif self.number_bombs == 7:
						color = DARK_PURPLE
					else:
						color = BLACK
					surface.blit(font.render(str(self.number_bombs), False, color), [self.x+self.w//4, self.y-2])
		elif self.maybe:
			surface.blit(font.render('?', False, BLACK), [self.x+self.w//4, self.y-2])


class App:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Minesweeper")
		self.running = False
		self.grid	 = []
		self.nbomb 	 = NUMBER_OF_BOMBS
		self.size	 = GRID_SIZE
		self.width	 = WINDOW_W
		self.height	 = WINDOW_H
		self.rows	 = self.width // self.size
		self.cols	 = self.width // self.size
		self.font 	 = pygame.font.SysFont('Arial', self.size)
		self.surface = pygame.display.set_mode([self.width, self.height], pygame.HWSURFACE)

	def init(self):
		self.running = True
		for i in range(self.rows):
			self.grid.append([])
			for j in range(self.cols):
				self.grid[i].append( Cell(i, j, self.size) )

		self.populate_grid()

		for i in range(self.rows):
			for j in range(self.cols):
				self.count_bombs(self.grid[i][j])

	def populate_grid(self):
		options = []
		for i in range(self.rows):
			for j in range(self.cols):
				options.append((i, j))
		for n in range(self.nbomb):
			r = random.randint(0, len(options)-1)
			choice = options.pop(r)
			i = choice[0]
			j = choice[1]
			self.grid[i][j].bomb = True

	def count_bombs(self, cell):
		if cell.bomb:
			return -1
		count = 0
		for xoff in (-1, 0, 1):
			for yoff in (-1, 0, 1):
				i = xoff + cell.i
				j = yoff + cell.j
				if i > -1 and i < self.rows and j > -1 and j < self.cols:
					if self.grid[i][j].bomb:
						count += 1
		cell.number_bombs = count

	def victory(self):
		for row in self.grid:
			for cell in row:
				cell.deactivated = True
				cell.reveal()

	def gameover(self):
		for row in self.grid:
			for cell in row:
				cell.reveal()

	def reveal(self, cell):
		cell.reveal()
		if cell.bomb:
			cell.exploded = True
			self.gameover()
		if cell.number_bombs == 0:
			self.flood_fill(cell)

	def flood_fill(self, cell):
		for xoff in (-1, 0, 1):
			for yoff in (-1, 0, 1):
				i = xoff + cell.i
				j = yoff + cell.j
				if i > -1 and i < self.rows and j > -1 and j < self.cols:
					c = self.grid[i][j]
					if not c.revealed:
						self.reveal(c)

	def event(self, event):
		if event.type == QUIT:
			self.running = False

		if event.type == MOUSEBUTTONDOWN:
			i = event.pos[0] // self.size
			j = event.pos[1] // self.size
			cell = self.grid[i][j]
			if event.button == 1 and not cell.revealed:
				self.reveal(cell)
			elif event.button == 3:
				cell.maybe = not cell.maybe

	def update(self):
		cont = 0
		for row in self.grid:
			for cell in row:
				if cell.revealed:
					cont += 1
		if cont == self.rows * self.cols - self.nbomb:
			self.victory()

	def draw(self):
		self.surface.fill((255, 255, 255))
		for line in self.grid:
			for cell in line:
				cell.draw(self.surface, self.font)
		pygame.display.flip()

	def cleanup(self):
		pygame.quit()
		quit()

	def execute(self):
		if self.init() == False:
			self.running = False
		while self.running:
			for event in pygame.event.get():
				self.event(event)
			self.update()
			self.draw()
		self.cleanup()


if __name__ == "__main__":
	game = App()
	game.execute()