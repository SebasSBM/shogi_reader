#!/usr/bin/env python
# * coding: utf-8 *

import os, pygame
from managers import *

# *** Constants ***
MAINPATH = os.path.dirname(os.path.abspath(__file__)) + '/'

# width, height = 1200,760
SCREEN = pygame.display.set_mode((1200, 760))
FONT = pygame.font.SysFont("monospace", 18)
