import pygame
import sys
import os
from pygame.locals import *

white = (255, 255, 255);
black = (0, 0, 0);

class Plane:
    def __init__(self):
        self.city_count = 0
        self.cities = dict()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        pygame.display.set_caption('TSP-toy')
        self.screen = pygame.display.set_mode((640, 480), 0, 0)
        self.screen.fill(white)
        self.button = pygame.Rect(0, 0, 66, 33)
        pygame.draw.rect(self.screen, [0, 0, 0], self.button, 1)
        self.font = pygame.font.SysFont('Arial', 25)
        self.screen.blit(self.font.render('Solve', True, black), (1, 1))
        self.screen.blit(self.font.render('Draw cities by clicking the mouse', True, black), (1, 450))

    def draw_pixel(self, pos):
        pygame.draw.circle(self.screen, black, pos, 5)
        self.cities[self.city_count] = pos
        self.city_count += 1

    def draw_pixels(self):
        drawing = True
        while drawing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit();
                    sys.exit();
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.button.collidepoint(pos):
                        drawing = False
                    else:
                        self.draw_pixel(pos)
            pygame.display.update()

    def draw_route(self, order):
        self.screen.fill(white)
        for i in range(0, self.city_count):
            pygame.draw.circle(self.screen, black, self.cities[i], 5)
        for i in range(0, len(order)-1):
            pygame.draw.line(self.screen, black, self.cities[order[i]], self.cities[order[i+1]])
        pygame.display.update()