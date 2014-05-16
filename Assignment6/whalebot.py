from random import choice
from time import sleep

from common import Model
from network import Handler, poll
from pygame import Rect, init as init_pygame
from pygame.display import set_mode, update as update_pygame_display
from pygame.draw import rect as draw_rect
from pygame.event import get as get_pygame_events
from pygame.time import Clock


################### CONTROLLER #############################

class RandomBotController():
    def __init__(self, m):
        self.m = m
        self.cmds = ['up', 'down', 'left', 'right']
        
    def poll(self):
        self.m.do_cmd(choice(self.cmds))
        
################### CONTROLLER #############################

class SmartBotController():
    def __init__(self, m):
        self.m = m
        
    def poll(self):
        p = self.m.pellets[0]  # always target the first pellet
        b = self.m.mybox
        if p[0] > b[0]:
            cmd = 'right'
        elif p[0] + p[2] < b[0]: # p[2] to avoid stuttering left-right movement
            cmd = 'left'
        elif p[1] > b[1]:
            cmd = 'down'
        else:
            cmd = 'up'
        self.m.do_cmd(cmd)
        
################### NETWORK CONTROLLER #############################
class NetworkController(Handler):
    def on_msg(self, data):
        global borders, pellets, players, myname
        borders = [make_rect(b) for b in data['borders']]
        pellets = [make_rect(p) for p in data['pellets']]
        players = {name: make_rect(p) for name, p in data['players'].items()}
        myname = data['myname']

################### CONSOLE VIEW #############################

class ConsoleView():
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.frame_freq = 20
        self.frame_count = 0
        
    def display(self):
        self.frame_count += 1
        if self.frame_count == self.frame_freq:
            self.frame_count = 0
            b = self.m.mybox
            print 'Position: %d, %d' % (b[0], b[1])


################### PYGAME VIEW #############################
# this view is only here in case you want to see how the bot behaves

import pygame

class PygameView():
    
    def __init__(self, m):
        self.m = m
        pygame.init()
        self.screen = pygame.display.set_mode((400, 300))
        
    def display(self):
        pygame.event.pump()
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
        
################### LOOP #############################

model = Model()
c = RandomBotController(model)
v = ConsoleView(model)
#v2 = PygameView(model)

def make_rect(quad):
    x, y, w, h = quad
    return Rect(x, y, w, h)

client = NetworkController('localhost',8888)

borders = []
pellets = []
players = {}
myname = None
clock = Clock()

while(borders == []):
    poll()
    print "Waiting for server.."
    
print "Successfully connected to server!"

model = Model()
c = SmartBotController(model)
v = ConsoleView(model)
v2 = PygameView(model)

while not model.game_over:
    sleep(0.02)
    c.poll()
    model.update()
    v.display()
    v2.display()