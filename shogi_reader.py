#!/usr/bin/env python
# * coding: utf-8 *

"""
    Copyright (C) 2014-2016  Sebastián Bover Mota <sebassbm.info@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
    The main script. It reads shogi games recorded with Western Notation
    and makes them easy to replay.

    Control keys:
        D / → -> Forward
        A / ← -> Backwards
        R -> Reverse board

    Open the files in "games_recorded" directory to see how it works.
"""

import pygame, tkMessageBox
import sys
import re

pygame.init()
from pygame.locals import *

from managers import MatrixManager, SpritesManager, Move
from globales import (PN, PB, SPN, SPB, LN, LB, SLN, SLB, NN, NB, SNN,
                      SNB, SN, SB, SSN, SSB, TN, TB, STN, STB, BN, BB,
                      SBN, SBB, GN, GB, KN, KB, SCREEN)
from globalvars import history, lamesa, partida, rawgame, game_data, matrix
from funciones import redraw, check_legal_destiny

PROMOTABLE = [PN,PB,LN,LB,NN,NB,SN,SB,TN,TB,BN,BB]
PROMOTED_KINDS = [SPN,SPB,SLN,SLB,SNN,SNB,SSN,SSB,STN,STB,SBN,SBB]
CONVERT_KIND = { 'Pn': PN, 'Pb': PB,
                 'Ln': LN, 'Lb': LB,
                 'Nn': NN, 'Nb': NB,
                 'Sn': SN, 'Sb': SB,
                 'Gn': GN, 'Gb': GB,
                 'Rn': TN, 'Rb': TB,
                 'Bn': BN, 'Bb': BB,
                 'Kn': KN, 'Kb': KB,
                 '+Pn': SPN, '+Pb': SPB,
                 '+Ln': SLN, '+Lb': SLB,
                 '+Nn': SNN, '+Nb': SNB,
                 '+Sn': SSN, '+Sb': SSB,
                 '+Rn': STN, '+Rb': STB,
                 '+Bn': SBN, '+Bb': SBB }

#reloj = pygame.time.Clock()

### Positions sheet
#
# 9-1 -> 21, 21
# 9-2 -> 92, 21// <- Desplazamiento vertical
#
# 8-1 -> 21, 92// <- Desplazamiento horizontal
#
###
#

"""
    ALGORITHM TO READ NOTATION AND TRANSFORM IT INTO DATA EXECUTABLE
    FORWARD AND BACKWARDS
"""

pygame.display.set_caption("ShogiReader - Reproductor de partidas grabadas")

# *** POSITIONS TABLE and Pieces arrays ***
#matrix = MatrixManager()

# *** Load input file ***
movs = game_data.movs.splitlines()

partida.close()
redraw()
reg = re.compile(r"""^\s*(?P<move_num>\d+)
                     \s*-\s*(?P<piece>\+?[PLNSGKRB])(?P<from>\d[a-i])?
                     (?P<action>[-x*])
                     (?P<to>\d[a-i][=+]?)$""", re.VERBOSE)
error_cnt = 0

# This loop transforms the notation into Move instances
for move in movs:
    move_to_add = None
    action = None
    promoting = False
    piece_respawn = [None,None,None]
    piece_x = 0
    piece_y = 0
    frag = reg.match(move)
    num_g = frag.group('move_num')
    piece_g = frag.group('piece')
    from_g = frag.group('from')
    to_g = frag.group('to')
    action_g = frag.group('action')
    destiny = [lamesa.coords_x[to_g[0]], lamesa.coords_y[to_g[1]]]
    destiny_h = to_g
    kind = piece_g
    if to_g.endswith('+'):
        promoting = True
    if from_g is not None:
        piece_x = lamesa.coords_x[from_g[0]]
        piece_y = lamesa.coords_y[from_g[1]]
    if action_g == 'x':
        action = 1
    elif action_g == '*':
        action = 2
    elif action_g == '-':
        action = 0
    sente = int(num_g) % 2 == 1
    possible_moves = 0
    if sente:
        player = 'n'
    else:
        player = 'b'
    dry = CONVERT_KIND[kind+player]

    # Handle piece capture
    if action == 1:
        found = False
        while not found:
            for sho in xrange(0,28):
                for k, e in lamesa.lista[sho].items():
                    if e == destiny:
                        del lamesa.lista[sho][k]
                        fres = (sho if not sho in
                                 PROMOTED_KINDS else sho - 2)
                        fres += -1 if sente else 1
                        if fres not in [KN, KB]:
                            lamesa.r[fres] += 1
                        piece_respawn[0] = sho
                        piece_respawn[1] = k
                        piece_respawn[2] = [destiny_h[0], destiny_h[1]]
                        found = True
                        break

    # Case: starting coords of piece not provided
    if piece_x == 0 and action != 2:
        for k, piece in lamesa.lista[dry].items():
            if check_legal_destiny(dry, piece, destiny, destiny_h):
                possible_moves += 1
                move_to_add = Move(dry, k, [destiny[0]-piece[0],
                                   destiny[1]-piece[1]], action,
                                   promoting, piece_respawn)
                matrix.empty(
                        matrix.get_hcoords(lamesa.lista[dry][k])
                )
                lamesa.lista[dry][k] = destiny
                matrix.fill(destiny_h)
                if promoting and dry in PROMOTABLE:
                    del lamesa.lista[dry][k]
                    lamesa.lista[dry+2][k] = destiny
    # Case: initial piece coords provided AND it's not a drop
    elif action != 2:
        for k, piece in lamesa.lista[dry].items():
            if piece[0] == piece_x and piece[1] == piece_y:
                if matrix.check(dry, matrix.get_hcoords(piece),
                                                    destiny_h):
                    move_to_add = Move(dry, k, [destiny[0]-piece[0],
                                       destiny[1]-piece[1]], action,
                                       promoting, piece_respawn)
                    matrix.empty(
                            matrix.get_hcoords(lamesa.lista[dry][k])
                    )
                    lamesa.lista[dry][k] = destiny
                    matrix.fill(destiny_h)
                    if promoting and dry in PROMOTABLE:
                        del lamesa.lista[dry][k]
                        lamesa.lista[dry+2][k] = destiny
                    break
    # Case: Action=2 (piece drop)
    elif kind[0] != '+':
        move_to_add = Move(dry, lamesa.cnt[dry], destiny_h,
                           action, promoting, piece_respawn)
        lamesa.lista[dry][lamesa.cnt[dry]] = destiny
        lamesa.cnt[dry] += 1
        lamesa.r[dry] -= 1

    #
    # TODO Check legal move -> not perfect yet
    if move_to_add != None:
        history.append(move_to_add)
    elif error_cnt == 0:
        error_expl = "The movement num."+str(len(history))
        error_expl+= " is not a legal move.\n\n"
        error_expl+= move + "\n\n"
        error_expl+= "This will cause errors replaying the game."
        tkMessageBox.showwarning("ILLEGAL MOVE", error_expl)
        error_cnt += 1
    # Ambiguity warning
    if possible_moves > 1 and error_cnt == 0:
        error_expl = "The notation in movement num."+str(len(history))
        error_expl+= " is ambiguous.\n\n"
        error_expl+= move + "\n\n"
        error_expl+= "This means that more than one piece can perform that"
        error_expl+= " move in that situation, and may cause errors while"
        error_expl+= " replaying the game. To prevent this, use"
        error_expl+= " desambiguation. For example:\n\n"
        error_expl+= "    G4i-5h instead of G-5h will specify that the gold"
        error_expl+= " to be moved is the one in 4i square."
        tkMessageBox.showwarning("AMBIGUOUS NOTATION", error_expl)
        error_cnt += 1


# *** From here, the history array is full of Move instances.
# *** So we restart the board to start drawing with pygame
sprites = SpritesManager()
max_history = len(history)
from funciones import (move_forward, previous_highlight, move_back,
                       show_names, get_pos)

# *** Pieces arrays *** -> restart
lamesa.begin()
show_names()
matrix = None
cnt_fw = 0
cnt_bw = 0
hold_fw = False
hold_bw = False
delay = 10

# Captured pieces positioning
RES_UP = {
    0:(25,21),
    4:(25,92),
    8:(136,92),
    12:(25,163),
    24:(136,163),
    16:(25,234),
    20:(116,234)
}
RES_DOWN = {
    0:(940,375),
    4:(940,446),
    8:(1051,446),
    12:(940,517),
    24:(1051,517),
    16:(940,588),
    20:(1031,588)
}

# Main loop to blit on the screen
while True:
    # Hold mode -> TODO Try to implement it correctly
    '''
    if hold_fw:
        cnt_fw += 1
        if cnt_fw >= 10 and pos < max_history:
            redraw()
            show_names()
            move_forward()
    if hold_bw:
        cnt_bw += 1
        if cnt_bw >= 10 and pos > 0:
            redraw()
            show_names()
            move_back()
    '''

    # Optimizing CPU consumption
    event = pygame.event.wait()
#    for event in pygame.event.get():
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == KEYDOWN and event.key == K_ESCAPE:
        sys.exit()
    elif event.type == KEYDOWN and (event.key == K_d or event.key == K_RIGHT
                                    ) and get_pos() < max_history:
        redraw()
        show_names()
        move_forward()
        hold_fw = True
        if cnt_fw < 10:
            cnt_fw += 1
    elif event.type == KEYUP and (event.key == K_d or event.key == K_RIGHT):
        hold_fw = False
        cnt_fw = 0
    elif event.type == KEYDOWN and (event.key == K_a or event.key == K_LEFT
                                    ) and get_pos() > 0:
        redraw()
        show_names()
        move_back()
        hold_bw = True
        if cnt_bw < 10:
            cnt_bw += 1
    elif event.type == KEYUP and (event.key == K_a or event.key == K_LEFT):
        hold_bw = False
        cnt_bw = 0
    elif event.type == KEYDOWN and event.key == K_r:
        lamesa.revert()
        redraw()
        show_names()
        sprites.revert(lamesa.reverted)
        previous_highlight(get_pos())

#        elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
#            silent.play()
#        elif event.type == KEYDOWN and event.key == K_SPACE:
#            pygame.image.save(screen, "screenshot.png")

#    mx,my = pygame.mouse.get_pos()
#    pygame.draw.line(SCREEN, (0,0,0), (20,20), (mx,my))

    # *** Captured pieces display ***
    if lamesa.reverted == 1:
        res_n = RES_DOWN
        res_b = RES_UP
    else:
        res_b = RES_DOWN
        res_n = RES_UP

    # Blit captured pieces
    kinds = [PN,PB,LN,LB,NN,NB,SN,SB,GN,GB,TN,TB,BN,BB]
    for kind in kinds:
        res = res_n if kind % 2 == 0 else res_b
        ri = kind - 1 if kind % 2 == 1 else kind
        for i in xrange(0, lamesa.r[kind]):
            mod = i * 10
            SCREEN.blit(sprites.imgs[kind], (res[ri][0]+mod, res[ri][1]))


    if lamesa.reverted == 1:
        comp_b = 2
        comp_n = 0
    else:
        comp_n = 2
        comp_b = 0

    # Blit in-board pieces
    for kind in xrange(0,28):
        comp = comp_n if kind % 2 == 0 else comp_b
        for k, piece in lamesa.lista[kind].items():
            SCREEN.blit(sprites.imgs[kind], (piece[0]-comp, piece[1]-comp))

#    reloj.tick(10)
    pygame.display.flip()
# una mas eficiente, que no actualiza la pantalla entera. busca sobre ésta:
# pygame.display.update()
