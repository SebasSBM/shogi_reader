#!/usr/bin/env python
# * coding: utf-8 *

import os, pygame

# *** Constants ***
MAINPATH = os.path.dirname(os.path.abspath(__file__)) + '/'

# width, height = 1200,760
SCREEN = pygame.display.set_mode((1200, 760))
FONT = pygame.font.SysFont("monospace", 18)

PN = 0
PB = 1
SPN = 2
SPB = 3
LN = 4
LB = 5
SLN = 6
SLB = 7
NN = 8
NB = 9
SNN = 10
SNB = 11
SN = 12
SB = 13
SSN = 14
SSB = 15
TN = 16
TB = 17
STN = 18
STB = 19
BN = 20
BB = 21
SBN = 22
SBB = 23
GN = 24
GB = 25
KN = 26
KB = 27
