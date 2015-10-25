#!/usr/bin/env python
# coding: utf-8

"""
    Copyright (C) 2014  Sebastián Bover Mota <sebassbm.info@gmail.com>

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

import pygame
import sys
import re

pygame.init()
from pygame.locals import *
from managers import *
from globales import *
from globalvars import history, lamesa, partida, rawgame, game_data
from funciones import redraw

#reloj = pygame.time.Clock()

pygame.display.set_caption("ShogiReader - Reproductor de partidas grabadas")

# *** POSITIONS TABLE and Pieces arrays ***
matrix = matrix_manager()

# *** Load input file ***
movs = game_data.movs.splitlines()

partida.close()
redraw()


### Positions sheet
#
# 9-1 -> 21, 21
# 9-2 -> 92, 21// <- Desplazamiento vertical
#
# 8-1 -> 21, 92// <- Desplazamiento horizontal
#
###
#

# *** ALGORITHM TO READ NOTATION AND TRANSFORM IT INTO DATA EXECUTABLE FORWARD AND BACKWARDS ***

reg = re.compile(r"""^\s*(?P<move_num>\d+)
                     \s*-\s*(?P<piece>\+?[PLNSGKRB])(?P<from>\d[a-i])?
                     (?P<action>[-x*])
                     (?P<to>\d[a-i][=+]?)$""", re.VERBOSE)
error_cnt = 0

for move in movs:
    move_to_add = None
    action = None
    promoting = False
    piece_respawn = ''
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

    if action == 1:
        if int(num_g) % 2 == 1: #Negras
            found = False
            while not found:
                for k, e in lamesa.lista[PB].items():
                    if e == destiny:
                        del lamesa.lista[PB][k]
                        lamesa.rpn += 1
                        piece_respawn = 'lista[PB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SPB].items():
                    if e == destiny:
                        del lamesa.lista[SPB][k]
                        lamesa.rpn += 1
                        piece_respawn = 'lista[SPB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[LB].items():
                    if e == destiny:
                        del lamesa.lista[LB][k]
                        lamesa.rln += 1
                        piece_respawn = 'lista[LB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SLB].items():
                    if e == destiny:
                        del lamesa.lista[SLB][k]
                        lamesa.rln += 1
                        piece_respawn = 'lista[SLB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[NB].items():
                    if e == destiny:
                        del lamesa.lista[NB][k]
                        lamesa.rnn += 1
                        piece_respawn = 'lista[NB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SNB].items():
                    if e == destiny:
                        del lamesa.lista[SNB][k]
                        lamesa.rnn += 1
                        piece_respawn = 'lista[SNB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SB].items():
                    if e == destiny:
                        del lamesa.lista[SB][k]
                        lamesa.rsn += 1
                        piece_respawn = 'lista[SB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SSB].items():
                    if e == destiny:
                        del lamesa.lista[SSB][k]
                        lamesa.rsn += 1
                        piece_respawn = 'lista[SSB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[GB].items():
                    if e == destiny:
                        del lamesa.lista[GB][k]
                        lamesa.rgn += 1
                        piece_respawn = 'lista[GB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[TB].items():
                    if e == destiny:
                        del lamesa.lista[TB][k]
                        lamesa.rtn += 1
                        piece_respawn = 'lista[TB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[STB].items():
                    if e == destiny:
                        del lamesa.lista[STB][k]
                        lamesa.rtn += 1
                        piece_respawn = 'lista[STB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[BB].items():
                    if e == destiny:
                        del lamesa.lista[BB][k]
                        lamesa.rbn += 1
                        piece_respawn = 'lista[BB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SBB].items():
                    if e == destiny:
                        del lamesa.lista[SBB][k]
                        lamesa.rbn += 1
                        piece_respawn = 'lista[SBB]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
        else: # Blancas
            found = False
            while not found:
                for k, e in lamesa.lista[PN].items():
                    if e == destiny:
                        del lamesa.lista[PN][k]
                        lamesa.rpb += 1
                        piece_respawn = 'lista[PN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SPN].items():
                    if e == destiny:
                        del lamesa.lista[SPN][k]
                        lamesa.rpb += 1
                        piece_respawn = 'lista[SPN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[LN].items():
                    if e == destiny:
                        del lamesa.lista[LN][k]
                        lamesa.rlb += 1
                        piece_respawn = 'lista[LN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SLN].items():
                    if e == destiny:
                        del lamesa.lista[SLN][k]
                        lamesa.rlb += 1
                        piece_respawn = 'lista[SLN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[NN].items():
                    if e == destiny:
                        del lamesa.lista[NN][k]
                        lamesa.rnb += 1
                        piece_respawn = 'lista[NN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SNN].items():
                    if e == destiny:
                        del lamesa.lista[SNN][k]
                        lamesa.rnb += 1
                        piece_respawn = 'lista[SNN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SN].items():
                    if e == destiny:
                        del lamesa.lista[SN][k]
                        lamesa.rsb += 1
                        piece_respawn = 'lista[SN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SSN].items():
                    if e == destiny:
                        del lamesa.lista[SSN][k]
                        lamesa.rsb += 1
                        piece_respawn = 'lista[SSN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[GN].items():
                    if e == destiny:
                        del lamesa.lista[GN][k]
                        lamesa.rgb += 1
                        piece_respawn = 'lista[GN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[TN].items():
                    if e == destiny:
                        del lamesa.lista[TN][k]
                        lamesa.rtb += 1
                        piece_respawn = 'lista[TN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[STN].items():
                    if e == destiny:
                        del lamesa.lista[STN][k]
                        lamesa.rtb += 1
                        piece_respawn = 'lista[STN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[BN].items():
                    if e == destiny:
                        del lamesa.lista[BN][k]
                        lamesa.rbb += 1
                        piece_respawn = 'lista[BN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista[SBN].items():
                    if e == destiny:
                        del lamesa.lista[SBN][k]
                        lamesa.rbb += 1
                        piece_respawn = 'lista[SBN]['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break

    possible_moves = 0
    if piece_x == 0 and action != 2:
        if int(num_g) % 2 == 1: #Negras
            if kind == 'P':
                for k, pn in lamesa.lista[PN].items():
                    if destiny[0] == pn[0] and destiny[1] == pn[1]-71:
                        possible_moves += 1
                        move_to_add = (['lista[PN]['+(str)(k)+']', [0, -71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[PN][k])
                        )
                        lamesa.lista[PN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[PN][k]
                            lamesa.lista[SPN][k] = destiny
            if kind == 'L':
                for k, ln in lamesa.lista[LN].items():
                    if destiny[0] == ln[0] and destiny[1] < ln[1]:
                        if matrix.check_ln(matrix.get_hcoords(ln), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[LN]['+(str)(k)+']',
                                           [0,destiny[1]-ln[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[LN][k])
                            )
                            lamesa.lista[LN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[LN][k]
                                lamesa.lista[SLN][k] = destiny
            if kind == 'N':
                for k, nn in lamesa.lista[NN].items():
                    if (destiny[0] == nn[0]+71 or
                            destiny[0] == nn[0]-71) and (destiny[1] ==
                            nn[1]-142):
                        possible_moves += 1
                        move_to_add = (['lista[NN]['+(str)(k)+']',
                                       [destiny[0]-nn[0], destiny[1]-nn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[NN][k])
                        )
                        lamesa.lista[NN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[NN][k]
                            lamesa.lista[SNN][k] = destiny
            if kind == 'S':
                for k, sn in lamesa.lista[SN].items():
                    if (destiny[0] <= sn[0]+71 and destiny[0] >= sn[0]-71 and
                            destiny[1] == sn[1]-71) or (
                             (destiny[0] == sn[0]+71 or
                             destiny[0] == sn[0]-71) and
                            destiny[1] == sn[1]+71):
                        possible_moves += 1
                        move_to_add = (['lista[SN]['+(str)(k)+']',
                                       [destiny[0]-sn[0],destiny[1]-sn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[SN][k])
                        )
                        lamesa.lista[SN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[SN][k]
                            lamesa.lista[SSN][k] = destiny
            if kind == 'G':
                for k, gn in lamesa.lista[GN].items():
                    if (destiny[0] <= gn[0]+71 and destiny[0] >= gn[0]-71 and
                            destiny[1] == gn[1]-71) or ((destiny[0] ==
                            gn[0]+71 or destiny[0] == gn[0]-71)
                            and destiny[1] == gn[1]) or (destiny[0] ==
                            gn[0] and destiny[1] == gn[1]+71):
                        possible_moves += 1
                        move_to_add = (['lista[GN]['+(str)(k)+']',
                                       [destiny[0]-gn[0],destiny[1]-gn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[GN][k])
                        )
                        lamesa.lista[GN][k] = destiny
                        matrix.fill(destiny_h)
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].upper()
                statem = 'for k, j in lamesa.lista[S'+mem+'N].items():\n'
                statem+= '    if (destiny[0] <= j[0]+71 and destiny[0] >='
                statem+= '            j[0]-71 and destiny[1] == j[1]-71) or ('
                statem+= '            (destiny[0] == j[0]+71 or destiny[0] =='
                statem+= '             j[0]-71) and destiny[1] == j[1]) or ('
                statem+= '             destiny[0] == j[0] and destiny[1] =='
                statem+= '             j[1]+71):\n'
                statem+= '        possible_moves += 1\n'
                statem+= '        move_to_add=["lista[S'+mem+'N]["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'N][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'N][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista[TN].items():
                    if (destiny[0] == tn[0]) != (destiny[1] == tn[1]):
                        if matrix.check_t(matrix.get_hcoords(tn), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[TN]['+(str)(k)+']',
                                           [destiny[0]-tn[0],
                                            destiny[1]-tn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[TN][k])
                            )
                            lamesa.lista[TN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[TN][k]
                                lamesa.lista[STN][k] = destiny
            if kind == '+R':
                for k, stn in lamesa.lista[STN].items():
                    if ((destiny[0] == stn[0]) != (destiny[1] == stn[1])) or (
                            destiny[0] <= stn[0]+71 and destiny[0] >=
                            stn[0]-71 and destiny[1] <= stn[1]+71 and
                            destiny[1] >= stn[1]-71):
                        if ((destiny[0] == stn[0]) != (destiny[1] ==
                                  stn[1]) and matrix.check_t(
                                        matrix.get_hcoords(stn),
                                        destiny_h)) or not((destiny[0] ==
                                   stn[0]) != (destiny[1] == stn[1])):
                            possible_moves += 1
                            move_to_add = (['lista[STN]['+(str)(k)+']',
                                           [destiny[0]-stn[0],
                                            destiny[1]-stn[1]],
                                            action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STN][k])
                            )
                            lamesa.lista[STN][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bn in lamesa.lista[BN].items():
                    if abs(destiny[0]-bn[0]) == abs(destiny[1]-bn[1]):
                        if matrix.check_b(matrix.get_hcoords(bn), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[BN]['+(str)(k)+']',
                                           [destiny[0]-bn[0],destiny[1]-bn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[BN][k])
                            )
                            lamesa.lista[BN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[BN][k]
                                lamesa.lista[SBN][k] = destiny
            if kind == '+B':
                for k, sbn in lamesa.lista[SBN].items():
                    if (abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) or (
                           destiny[0] <= sbn[0]+71 and destiny[0] >=
                           sbn[0]-71 and destiny[1] <= sbn[1]+71 and
                           destiny[1] >= sbn[1]-71):
                        if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbn),
                              destiny_h)) or not (abs(destiny[0]-sbn[0]) ==
                                abs(destiny[1]-sbn[1])):
                            possible_moves += 1
                            move_to_add = (['lista[SBN]['+(str)(k)+']',
                                           [destiny[0]-sbn[0],
                                            destiny[1]-sbn[1]],
                                            action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBN][k])
                            )
                            lamesa.lista[SBN][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'K':
                if (destiny[0] <= lamesa.rey_n[0]+71 and
                        destiny[0] >= lamesa.rey_n[0]-71 and
                        destiny[1] <= lamesa.rey_n[1]+71 and
                        destiny[1] >= lamesa.rey_n[1]-71):
                    move_to_add = (['rey_n',[destiny[0]-lamesa.rey_n[0],
                                   destiny[1]-lamesa.rey_n[1]],
                                   action, promoting, piece_respawn])
                    matrix.empty(matrix.get_hcoords(lamesa.rey_n))
                    lamesa.rey_n = destiny
                    matrix.fill(destiny_h)
        else: #Blancas
            if kind == 'P':
                for k, pb in lamesa.lista[PB].items():
                    if destiny[0] == pb[0] and destiny[1] == pb[1]+71:
                        possible_moves += 1
                        move_to_add = (['lista[PB]['+(str)(k)+']',[0, 71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[PB][k])
                        )
                        lamesa.lista[PB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[PB][k]
                            lamesa.lista[SPB][k] = destiny
            if kind == 'L':
                for k, lb in lamesa.lista[LB].items():
                    if destiny[0] == lb[0] and destiny[1] > lb[1]:
                        if matrix.check_lb(matrix.get_hcoords(lb), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[LB]['+(str)(k)+']',
                                           [0,destiny[1]-lb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[LB][k])
                            )
                            lamesa.lista[LB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[LB][k]
                                lamesa.lista[SLB][k] = destiny
            if kind == 'N':
                for k, nb in lamesa.lista[NB].items():
                    if (destiny[0] == nb[0]+71 or destiny[0] == nb[0]-71) and (
                               destiny[1] == nb[1]+142):
                        possible_moves += 1
                        move_to_add = (['lista[NB]['+(str)(k)+']',
                                       [destiny[0]-nb[0],destiny[1]-nb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[NB][k])
                        )
                        lamesa.lista[NB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[NB][k]
                            lamesa.lista[SNB][k] = destiny
            if kind == 'S':
                for k, sb in lamesa.lista[SB].items():
                    if (destiny[0] <= sb[0]+71 and destiny[0] >= sb[0]-71 and
                            destiny[1] == sb[1]+71) or (
                              (destiny[0] == sb[0]+71 or
                               destiny[0] == sb[0]-71) and
                              destiny[1] == sb[1]-71):
                        possible_moves += 1
                        move_to_add = (['lista[SB]['+(str)(k)+']',
                                       [destiny[0]-sb[0],destiny[1]-sb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[SB][k])
                        )
                        lamesa.lista[SB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[SB][k]
                            lamesa.lista[SSB][k] = destiny
            if kind == 'G':
                for k, gb in lamesa.lista[GB].items():
                    if (destiny[0] <= gb[0]+71 and destiny[0] >= gb[0]-71 and
                             destiny[1] == gb[1]+71) or (
                              (destiny[0] == gb[0]+71 or
                                destiny[0] == gb[0]-71) and
                              destiny[1] == gb[1]) or (destiny[0] == gb[0] and
                              destiny[1] == gb[1]-71):
                        possible_moves += 1
                        move_to_add = (['lista[GB]['+(str)(k)+']',
                                       [destiny[0]-gb[0],destiny[1]-gb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[GB][k])
                        )
                        lamesa.lista[GB][k] = destiny
                        matrix.fill(destiny_h)
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].upper()
                statem = 'for k, j in lamesa.lista[S'+mem+'B].items():\n'
                statem+= '    if (destiny[0] <= j[0]+71 and destiny[0] >='
                statem+= '            j[0]-71 and destiny[1] == j[1]+71) or ('
                statem+= '            (destiny[0] == j[0]+71 or destiny[0] =='
                statem+= '             j[0]-71) and destiny[1] == j[1]) or ('
                statem+= '             destiny[0] == j[0] and destiny[1] =='
                statem+= '             j[1]-71):\n'
                statem+= '        possible_moves += 1\n'
                statem+= '        move_to_add=["lista[S'+mem+'B]["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'B][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'B][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista[TB].items():
                    if (destiny[0] == tb[0]) != (destiny[1] == tb[1]):
                        if matrix.check_t(matrix.get_hcoords(tb),destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[TB]['+(str)(k)+']',
                                           [destiny[0]-tb[0],
                                            destiny[1]-tb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[TB][k])
                            )
                            lamesa.lista[TB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[TB][k]
                                lamesa.lista[STB][k] = destiny
            if kind == '+R':
                for k, stb in lamesa.lista[STB].items():
                    if ((destiny[0] == stb[0]) != (destiny[1] == stb[1])) or (
                            destiny[0] <= stb[0]+71 and destiny[0] >=
                            stb[0]-71 and destiny[1] <= stb[1]+71 and
                            destiny[1] >= stb[1]-71):
                        if ((destiny[0] == stb[0]) != (destiny[1] ==
                                  stb[1]) and matrix.check_t(
                                        matrix.get_hcoords(stb),
                                        destiny_h)) or not((destiny[0] ==
                                   stb[0]) != (destiny[1] == stb[1])):
                            possible_moves += 1
                            move_to_add = (['lista[STB]['+(str)(k)+']',
                                           [destiny[0]-stb[0],
                                            destiny[1]-stb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STB][k])
                            )
                            lamesa.lista[STB][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bb in lamesa.lista[BB].items():
                    if abs(destiny[0]-bb[0]) == abs(destiny[1]-bb[1]):
                        if matrix.check_b(matrix.get_hcoords(bb), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista[BB]['+(str)(k)+']',
                                           [destiny[0]-bb[0],
                                            destiny[1]-bb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[BB][k])
                            )
                            lamesa.lista[BB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[BB][k]
                                lamesa.lista[SBB][k] = destiny
            if kind == '+B':
                for k, sbb in lamesa.lista[SBB].items():
                    if (abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) or (
                           destiny[0] <= sbb[0]+71 and destiny[0] >=
                           sbb[0]-71 and destiny[1] <= sbb[1]+71 and
                           destiny[1] >= sbb[1]-71):
                        if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbb),
                              destiny_h)) or not (abs(destiny[0]-sbb[0]) ==
                                abs(destiny[1]-sbb[1])):
                            possible_moves += 1
                            move_to_add = (['lista[SBB]['+(str)(k)+']',
                                           [destiny[0]-sbb[0],
                                            destiny[1]-sbb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBB][k])
                            )
                            lamesa.lista[SBB][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'K':
                if (destiny[0] <= lamesa.rey_b[0]+71 and
                        destiny[0] >= lamesa.rey_b[0]-71 and
                        destiny[1] <= lamesa.rey_b[1]+71 and
                        destiny[1] >= lamesa.rey_b[1]-71):
                    move_to_add = (['rey_b',[destiny[0]-lamesa.rey_b[0],
                                   destiny[1]-lamesa.rey_b[1]],
                                   action, promoting, piece_respawn])
                    matrix.empty(matrix.get_hcoords(lamesa.rey_b))
                    lamesa.rey_b = destiny
                    matrix.fill(destiny_h)
    elif action != 2:
        if int(num_g) % 2 == 1: #Negras
            if kind == 'P':
                for k, pn in lamesa.lista[PN].items():
                    if pn[0] == piece_x and pn[1] == piece_y:
                        move_to_add = (['lista[PN]['+(str)(k)+']', [0,-71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[PN][k])
                        )
                        lamesa.lista[PN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[PN][k]
                            lamesa.lista[SPN][k] = destiny
                        break
            if kind == 'L':
                for k, ln in lamesa.lista[LN].items():
                    if ln[0] == piece_x and ln[1] == piece_y:
                        if matrix.check_ln(matrix.get_hcoords(ln), destiny_h):
                            move_to_add = (['lista[LN]['+(str)(k)+']',
                                           [0, destiny[1]-ln[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[LN][k])
                            )
                            lamesa.lista[LN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[LN][k]
                                lamesa.lista[SLN][k] = destiny
                            break
            if kind == 'N':
                for k, nn in lamesa.lista[NN].items():
                    if nn[0] == piece_x and nn[1] == piece_y:
                        move_to_add = (['lista[NN]['+(str)(k)+']',
                                       [destiny[0]-nn[0],
                                        destiny[1]-nn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[NN][k])
                        )
                        lamesa.lista[NN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[NN][k]
                            lamesa.lista[SNN][k] = destiny
                        break
            if kind == 'S':
                for k, sn in lamesa.lista[SN].items():
                    if sn[0] == piece_x and sn[1] == piece_y:
                        move_to_add = (['lista[SN]['+(str)(k)+']',
                                       [destiny[0]-sn[0],
                                        destiny[1]-sn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[SN][k])
                        )
                        lamesa.lista[SN][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[SN][k]
                            lamesa.lista[SSN][k] = destiny
                        break
            if kind == 'G':
                for k, gn in lamesa.lista[GN].items():
                    if gn[0] == piece_x and gn[1] == piece_y:
                        move_to_add = (['lista[GN]['+(str)(k)+']',
                                       [destiny[0]-gn[0], destiny[1]-gn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[GN][k])
                        )
                        lamesa.lista[GN][k] = destiny
                        matrix.fill(destiny_h)
                        break
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista[S'+mem+'N].items():\n'
                statem+= '    if j[0] == piece_x and j[1] == piece_y:\n'
                statem+= '        move_to_add=["lista[S'+mem+'N]["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'N][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'N][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista[TN].items():
                    if tn[0] == piece_x and tn[1] == piece_y:
                        if matrix.check_t(matrix.get_hcoords(tn), destiny_h):
                            move_to_add = (['lista[TN]['+(str)(k)+']',
                                           [destiny[0]-tn[0],
                                            destiny[1]-tn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[TN][k])
                            )
                            lamesa.lista[TN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[TN][k]
                                lamesa.lista[STN][k] = destiny
                            break
            if kind == '+R':
                for k, stn in lamesa.lista[STN].items():
                    if stn[0] == piece_x and stn[1] == piece_y:
                        if ((destiny[0] == stn[0]) != (destiny[1] == stn[1]
                            ) and matrix.check_t(matrix.get_hcoords(stn),
                              destiny_h)) or not ((destiny[0] == stn[0]) != (
                                destiny[1] == stn[1])):
                            move_to_add = (['lista[STN]['+(str)(k)+']',
                                           [destiny[0]-stn[0],
                                            destiny[1]-stn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STN][k])
                            )
                            lamesa.lista[STN][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bn in lamesa.lista[BN].items():
                    if bn[0] == piece_x and bn[1] == piece_y:
                        if matrix.check_b(matrix.get_hcoords(bn),destiny_h):
                            move_to_add = (['lista[BN]['+(str)(k)+']',
                                           [destiny[0]-bn[0],
                                            destiny[1]-bn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[BN][k])
                            )
                            lamesa.lista[BN][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[BN][k]
                                lamesa.lista[SBN][k] = destiny
                            break
            if kind == '+B':
                for k, sbn in lamesa.lista[SBN].items():
                    if sbn[0] == piece_x and sbn[1] == piece_y:
                        if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbn),
                                destiny_h)) or not (abs(destiny[0]-sbn[0]
                                ) == abs(destiny[1]-sbn[1])):
                            move_to_add = (['lista[SBN]['+(str)(k)+']',
                                           [destiny[0]-sbn[0],
                                            destiny[1]-sbn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBN][k])
                            )
                            lamesa.lista[SBN][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'K':
                if lamesa.rey_n[0] == piece_x and lamesa.rey_n[1] == piece_y:
                    move_to_add = (['rey_n',[destiny[0]-lamesa.rey_n[0],
                                   destiny[1]-lamesa.rey_n[1]],
                                   action, promoting, piece_respawn])
                    matrix.empty(matrix.get_hcoords(lamesa.rey_n))
                    lamesa.rey_n = destiny
                    matrix.fill(destiny_h)
        else: # Blancas
            if kind == 'P':
                for k, pb in lamesa.lista[PB].items():
                    if pb[0] == piece_x and pb[1] == piece_y:
                        move_to_add = (['lista[PB]['+(str)(k)+']',[0,+71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[PB][k])
                        )
                        lamesa.lista[PB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[PB][k]
                            lamesa.lista[SPB][k] = destiny
                        break
            if kind == 'L':
                for k, lb in lamesa.lista[LB].items():
                    if lb[0] == piece_x and lb[1] == piece_y:
                        if matrix.check_lb(matrix.get_hcoords(lb), destiny_h):
                            move_to_add = (['lista[LB]['+(str)(k)+']',
                                           [0, destiny[1]-lb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[LB][k])
                            )
                            lamesa.lista[LB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[LB][k]
                                lamesa.lista[SLB][k] = destiny
                            break
            if kind == 'N':
                for k, nb in lamesa.lista[NB].items():
                    if nb[0] == piece_x and nb[1] == piece_y:
                        move_to_add = (['lista[NB]['+(str)(k)+']',
                                       [destiny[0]-nb[0],
                                        destiny[1]-nb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[NB][k])
                        )
                        lamesa.lista[NB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[NB][k]
                            lamesa.lista[SNB][k] = destiny
                        break
            if kind == 'S':
                for k, sb in lamesa.lista[SB].items():
                    if sb[0] == piece_x and sb[1] == piece_y:
                        move_to_add = (['lista[SB]['+(str)(k)+']',
                                       [destiny[0]-sb[0],
                                        destiny[1]-sb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[SB][k])
                        )
                        lamesa.lista[SB][k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista[SB][k]
                            lamesa.lista[SSB][k] = destiny
                        break
            if kind == 'G':
                for k, gb in lamesa.lista[GB].items():
                    if gb[0] == piece_x and gb[1] == piece_y:
                        move_to_add = (['lista[GB]['+(str)(k)+']',
                                       [destiny[0]-gb[0],
                                        destiny[1]-gb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista[GB][k])
                        )
                        lamesa.lista[GB][k] = destiny
                        matrix.fill(destiny_h)
                        break
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista[S'+mem+'B].items():\n'
                statem+= '    if j[0] == piece_x and j[1] == piece_y:\n'
                statem+= '        move_to_add=["lista[S'+mem+'B]["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'B][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'B][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n\t\t'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista[TB].items():
                    if tb[0] == piece_x and tb[1] == piece_y:
                        if matrix.check_t(matrix.get_hcoords(tb),destiny_h):
                            move_to_add = (['lista[TB]['+(str)(k)+']',
                                           [destiny[0]-tb[0],
                                            destiny[1]-tb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[TB][k])
                            )
                            lamesa.lista[TB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[TB][k]
                                lamesa.lista[STB][k] = destiny
                            break
            if kind == '+R':
                for k, stb in lamesa.lista[STB].items():
                    if stb[0] == piece_x and stb[1] == piece_y:
                        if ((destiny[0] == stb[0]) != (destiny[1] == stb[1]
                            ) and matrix.check_t(matrix.get_hcoords(stb),
                              destiny_h)) or not ((destiny[0] == stb[0]) != (
                                destiny[1] == stb[1])):
                            move_to_add = (['lista[STB]['+(str)(k)+']',
                                           [destiny[0]-stb[0],
                                            destiny[1]-stb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STB][k])
                            )
                            lamesa.lista[STB][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bb in lamesa.lista[BB].items():
                    if bb[0] == piece_x and bb[1] == piece_y:
                        if matrix.check_b(matrix.get_hcoords(bb),destiny_h):
                            move_to_add = (['lista[BB]['+(str)(k)+']',
                                           [destiny[0]-bb[0],
                                            destiny[1]-bb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[BB][k])
                            )
                            lamesa.lista[BB][k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista[BB][k]
                                lamesa.lista[SBB][k] = destiny
                            break
            if kind == '+B':
                for k, sbb in lamesa.lista[SBB].items():
                    if sbb[0] == piece_x and sbb[1] == piece_y:
                        if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbb),
                                destiny_h) == True) or not(abs(destiny[0]-sbb[0]
                                ) == abs(destiny[1]-sbb[1])):
                            move_to_add = (['lista[SBB]['+(str)(k)+']',
                                           [destiny[0]-sbb[0],
                                            destiny[1]-sbb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBB][k])
                            )
                            lamesa.lista[SBB][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'K':
                if lamesa.rey_b[0] == piece_x and lamesa.rey_b[1] == piece_y:
                    move_to_add = (['rey_b',[destiny[0]-lamesa.rey_b[0],
                                   destiny[1]-lamesa.rey_b[1]],
                                   action, promoting, piece_respawn])
                    matrix.empty(matrix.get_hcoords(lamesa.rey_b))
                    lamesa.rey_b = destiny
                    matrix.fill(destiny_h)
    else: # Action=2 (reingreso)
        if int(num_g) % 2 == 1: #Negras
            player = 'n'
        else:
            player = 'b'

        if kind == 'P':
            if player == 'n':
                move_to_add = ([['pn',lamesa.cnt[PN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[PN][lamesa.cnt[PN]] = destiny
                lamesa.cnt[PN] += 1
                lamesa.rpn -= 1
            else:
                move_to_add = ([['pb',lamesa.cnt[PB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[PB][lamesa.cnt[PB]] = destiny
                lamesa.cnt[PB] += 1
                lamesa.rpb -= 1
        if kind == 'L':
            if player == 'n':
                move_to_add = ([['ln',lamesa.cnt[LN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[LN][lamesa.cnt[LN]] = destiny
                lamesa.cnt[LN] += 1
                lamesa.rln -= 1
            else:
                move_to_add = ([['lb',lamesa.cnt[LB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[LB][lamesa.cnt[LB]] = destiny
                lamesa.cnt[LB] += 1
                lamesa.rlb -= 1
        if kind == 'N':
            if player == 'n':
                move_to_add = ([['nn',lamesa.cnt[NN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[NN][lamesa.cnt[NN]] = destiny
                lamesa.cnt[NN] += 1
                lamesa.rnn -= 1
            else:
                move_to_add = ([['nb',lamesa.cnt[NB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[NB][lamesa.cnt[NB]] = destiny
                lamesa.cnt[NB] += 1
                lamesa.rnb -= 1
        if kind == 'S':
            if player == 'n':
                move_to_add = ([['sn',lamesa.cnt[SN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[SN][lamesa.cnt[SN]] = destiny
                lamesa.cnt[SN] += 1
                lamesa.rsn -= 1
            else:
                move_to_add = ([['sb',lamesa.cnt[SB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[SB][lamesa.cnt[SB]] = destiny
                lamesa.cnt[SB] += 1
                lamesa.rsb -= 1
        if kind == 'G':
            if player == 'n':
                move_to_add = ([['gn',lamesa.cnt[GN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[GN][lamesa.cnt[GN]] = destiny
                lamesa.cnt[GN] += 1
                lamesa.rgn -= 1
            else:
                move_to_add = ([['gb',lamesa.cnt[GB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[GB][lamesa.cnt[GB]] = destiny
                lamesa.cnt[GB] += 1
                lamesa.rgb -= 1
        if kind == 'R':
            if player == 'n':
                move_to_add = ([['tn',lamesa.cnt[TN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[TN][lamesa.cnt[TN]] = destiny
                lamesa.cnt[TN] += 1
                lamesa.rtn -= 1
            else:
                move_to_add = ([['tb',lamesa.cnt[TB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[TB][lamesa.cnt[TB]] = destiny
                lamesa.cnt[TB] += 1
                lamesa.rtb -= 1
        if kind == 'B':
            if player == 'n':
                move_to_add = ([['bn',lamesa.cnt[BN]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[BN][lamesa.cnt[BN]] = destiny
                lamesa.cnt[BN] += 1
                lamesa.rbn -= 1
            else:
                move_to_add = ([['bb',lamesa.cnt[BB]], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista[BB][lamesa.cnt[BB]] = destiny
                lamesa.cnt[BB] += 1
                lamesa.rbb -= 1
        matrix.fill(destiny_h)

    # TODO Check legal move
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
    if possible_moves > 1and error_cnt == 0:
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
        

    #Loading progress
    #print len(history)

# *** sprites ***
sprites = sprites_manager()

#pos = 0
max_history = len(history)
print max_history

# TODO:
# .History registries should be optimized to prevent the mess in
# . move_forward() and move backwards() to handle some extraordinary
# . situations. When I say "mess" I mean that some instructions are
# . excessively complicated I guess, they are doing
# . thing that I'm sure can be achieved in a more simple way.
from funciones import move_forward, previous_highlight, move_back, show_names


# *** Pieces arrays *** -> restart
lamesa.begin()
show_names()
matrix = None

from funciones import get_pos

cnt_fw = 0
cnt_bw = 0
hold_fw = False
hold_bw = False
delay = 10
while True:
#    global pos
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
        exec move_forward()
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
        exec move_back()
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
        # Invert sprites
        sprites.revert(lamesa.reverted)
        previous_highlight(get_pos())

#        elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
#            silent.play()
#        elif event.type == KEYDOWN and event.key == K_SPACE:
#            pygame.image.save(screen, "screenshot.png")

#    mx,my = pygame.mouse.get_pos()
#    pygame.draw.line(SCREEN, (0,0,0), (20,20), (mx,my))

    # *** Captured pieces display ***
    res_up = {
        'p':(25,21),
        'l':(25,92),
        'n':(136,92),
        's':(25,163),
        'g':(136,163),
        't':(25,234),
        'b':(116,234)
    }
    res_down = {
        'p':(940,375),
        'l':(940,446),
        'n':(1051,446),
        's':(940,517),
        'g':(1051,517),
        't':(940,588),
        'b':(1031,588)
    }
    if lamesa.reverted == 1:
        res_n = res_down
        res_b = res_up
    else:
        res_b = res_down
        res_n = res_up

    for i in xrange(0, lamesa.rpn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[PN], (res_n['p'][0]+mod, res_n['p'][1]))
    for i in xrange(0, lamesa.rpb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[PB], (res_b['p'][0]+mod, res_b['p'][1]))
    for i in xrange(0, lamesa.rln):
        mod = i * 10
        SCREEN.blit(sprites.imgs[LN], (res_n['l'][0]+mod, res_n['l'][1]))
    for i in xrange(0, lamesa.rlb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[LB], (res_b['l'][0]+mod, res_b['l'][1]))
    for i in xrange(0, lamesa.rnn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[NN], (res_n['n'][0]+mod, res_n['n'][1]))
    for i in xrange(0, lamesa.rnb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[NB], (res_b['n'][0]+mod, res_b['n'][1]))
    for i in xrange(0, lamesa.rsn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[SN], (res_n['s'][0]+mod, res_n['s'][1]))
    for i in xrange(0, lamesa.rsb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[SB], (res_b['s'][0]+mod, res_b['s'][1]))
    for i in xrange(0, lamesa.rgn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[GN], (res_n['g'][0]+mod, res_n['g'][1]))
    for i in xrange(0, lamesa.rgb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[GB], (res_b['g'][0]+mod, res_b['g'][1]))
    for i in xrange(0, lamesa.rtn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[TN], (res_n['t'][0]+mod, res_n['t'][1]))
    for i in xrange(0, lamesa.rtb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[TB], (res_b['t'][0]+mod, res_b['t'][1]))
    for i in xrange(0, lamesa.rbn):
        mod = i * 10
        SCREEN.blit(sprites.imgs[BN], (res_n['b'][0]+mod, res_n['b'][1]))
    for i in xrange(0, lamesa.rbb):
        mod = i * 10
        SCREEN.blit(sprites.imgs[BB], (res_b['b'][0]+mod, res_b['b'][1]))

    # *** This reads the current position of pieces to place them ***
    if lamesa.reverted == 1:
        comp_b = 2
        comp_n = 0
    else:
        comp_n = 2
        comp_b = 0
    for k, pn in lamesa.lista[PN].items():
        SCREEN.blit(sprites.imgs[PN], (pn[0]-comp_n, pn[1]-comp_n))
    for k, spn in lamesa.lista[SPN].items():
        SCREEN.blit(sprites.imgs[SPN], (spn[0]-comp_n, spn[1]-comp_n))
    for k, pb in lamesa.lista[PB].items():
        SCREEN.blit(sprites.imgs[PB], (pb[0]-comp_b, pb[1]-comp_b))
    for k, spb in lamesa.lista[SPB].items():
        SCREEN.blit(sprites.imgs[SPB], (spb[0]-comp_b, spb[1]-comp_b))
    for k, ln in lamesa.lista[LN].items():
        SCREEN.blit(sprites.imgs[LN], (ln[0]-comp_n, ln[1]-comp_n))
    for k, sln in lamesa.lista[SLN].items():
        SCREEN.blit(sprites.imgs[SLN], (sln[0]-comp_n, sln[1]-comp_n))
    for k, lb in lamesa.lista[LB].items():
        SCREEN.blit(sprites.imgs[LB], (lb[0]-comp_b, lb[1]-comp_b))
    for k, slb in lamesa.lista[SLB].items():
        SCREEN.blit(sprites.imgs[SLB], (slb[0]-comp_b, slb[1]-comp_b))
    for k, nn in lamesa.lista[NN].items():
        SCREEN.blit(sprites.imgs[NN], (nn[0]-comp_n, nn[1]-comp_n))
    for k, snn in lamesa.lista[SNN].items():
        SCREEN.blit(sprites.imgs[SNN], (snn[0]-comp_n, snn[1]-comp_n))
    for k, nb in lamesa.lista[NB].items():
        SCREEN.blit(sprites.imgs[NB], (nb[0]-comp_b, nb[1]-comp_b))
    for k, snb in lamesa.lista[SNB].items():
        SCREEN.blit(sprites.imgs[SNB], (snb[0]-comp_b, snb[1]-comp_b))
    for k, sn in lamesa.lista[SN].items():
        SCREEN.blit(sprites.imgs[SN], (sn[0]-comp_n, sn[1]-comp_n))
    for k, ssn in lamesa.lista[SSN].items():
        SCREEN.blit(sprites.imgs[SSN], (ssn[0]-comp_n, ssn[1]-comp_n))
    for k, sb in lamesa.lista[SB].items():
        SCREEN.blit(sprites.imgs[SB], (sb[0]-comp_b, sb[1]-comp_b))
    for k, ssb in lamesa.lista[SSB].items():
        SCREEN.blit(sprites.imgs[SSB], (ssb[0]-comp_b, ssb[1]-comp_b))
    for k, gn in lamesa.lista[GN].items():
        SCREEN.blit(sprites.imgs[GN], (gn[0]-comp_n, gn[1]-comp_n))
    for k, gb in lamesa.lista[GB].items():
        SCREEN.blit(sprites.imgs[GB], (gb[0]-comp_b, gb[1]-comp_b))
    for k, tn in lamesa.lista[TN].items():
        SCREEN.blit(sprites.imgs[TN], (tn[0]-comp_n, tn[1]-comp_n))
    for k, stn in lamesa.lista[STN].items():
        SCREEN.blit(sprites.imgs[STN], (stn[0]-comp_n, stn[1]-comp_n))
    for k, tb in lamesa.lista[TB].items():
        SCREEN.blit(sprites.imgs[TB], (tb[0]-comp_b, tb[1]-comp_b))
    for k, stb in lamesa.lista[STB].items():
        SCREEN.blit(sprites.imgs[STB], (stb[0]-comp_b, stb[1]-comp_b))
    for k, bn in lamesa.lista[BN].items():
        SCREEN.blit(sprites.imgs[BN], (bn[0]-comp_n, bn[1]-comp_n))
    try:
        for k, sbn in lamesa.lista[SBN].items():
            SCREEN.blit(sprites.imgs[SBN], (sbn[0]-comp_n, sbn[1]-comp_n))
    except AttributeError, e:
        print 'SBM_EYE: ', type(lamesa.lista[SBN])
        print '------->', lamesa.lista[SBN]
        raise e
    for k, bb in lamesa.lista[BB].items():
        SCREEN.blit(sprites.imgs[BB], (bb[0]-comp_b, bb[1]-comp_b))
    for k, sbb in lamesa.lista[SBB].items():
        SCREEN.blit(sprites.imgs[SBB], (sbb[0]-comp_b, sbb[1]-comp_b))
    SCREEN.blit(sprites.imgs[KN],
                (lamesa.rey_n[0]-comp_n, lamesa.rey_n[1]-comp_n))
    SCREEN.blit(sprites.imgs[KB],
                (lamesa.rey_b[0]-comp_b, lamesa.rey_b[1]-comp_b))

#    reloj.tick(10)
    pygame.display.flip()
# una mas eficiente, que no actualiza la pantalla entera. busca sobre ésta:
# pygame.display.update()
