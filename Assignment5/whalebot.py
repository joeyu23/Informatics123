from random import randint
from time import sleep
from common import Model
            

################### CONTROLLER #############################

import pygame
from pygame.locals import KEYDOWN, QUIT, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RCTRL, K_LCTRL, K_c

class Controller():
    def __init__(self, m):
        self.m = m
        pygame.init()
    
    def poll(self):
        cmd = None
        
        pelletPos = self.m.pellets[0]
        pelletPosX = pelletPos[0]
        pelletPosY = pelletPos[1]
        diffX = self.m.mybox[0] - pelletPosX
        diffY =  self.m.mybox[1] - pelletPosY
        if diffX > 0:
            cmd = 'left'
        else:
            diffX < 0
            cmd = 'right'
        if diffY > 0:
            cmd = 'up'
        else:
            diffY < 0
            cmd = 'down'
            
        for event in pygame.event.get():  # inputs
            keys = pygame.key.get_pressed()
            if event.type == QUIT:
                cmd = 'quit'
            if event.type == KEYDOWN:
                key = event.key
                if keys[K_LCTRL] and keys[K_c]:
                    cmd = 'quit'
                elif keys[K_RCTRL] and keys[K_c]:
                    cmd = 'quit'
        if cmd:
            self.m.do_cmd(cmd)
'''
            if event.type == KEYDOWN:
                key = event.key
                if key == K_ESCAPE:
                    cmd = 'quit'
                elif key == K_UP:
                    cmd = 'up'
                elif key == K_DOWN:
                    cmd = 'down'
                elif key == K_LEFT:
                    cmd = 'left'
                elif key == K_RIGHT:
                    cmd = 'right'
'''


################### VIEW #############################

class View():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        screen = self.screen
        borders = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in self.m.borders]
        pellets = [pygame.Rect(p[0], p[1], p[2], p[3]) for p in self.m.pellets]
        b = self.m.mybox
        myrect = pygame.Rect(b[0], b[1], b[2], b[3])
        screen.fill((0, 0, 64))  # dark blue
        pygame.draw.rect(screen, (0, 191, 255), myrect)  # Deep Sky Blue
        [pygame.draw.rect(screen, (255, 192, 203), p) for p in pellets]  # pink
        [pygame.draw.rect(screen, (0, 191, 255), b) for b in borders]  # red
        pygame.display.update()
        
class AlternateView():
    def __init__(self, m):
        self.frameCounter = 0
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
    
    def display(self):
        self.frameCounter = self.frameCounter + 1
        b = self.m.mybox
        if self.frameCounter % 50 == 0:
            print "Position:" , b[0], " , ", b[1]
            
            
################### LOOP #############################

model = Model()
c = Controller(model)
v = AlternateView(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()