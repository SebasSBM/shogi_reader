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
                for k, e in lamesa.lista_pb.items():
                    if e == destiny:
                        del lamesa.lista_pb[k]
                        lamesa.rpn += 1
                        piece_respawn = 'lista_pb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_spb.items():
                    if e == destiny:
                        del lamesa.lista_spb[k]
                        lamesa.rpn += 1
                        piece_respawn = 'lista_spb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_lb.items():
                    if e == destiny:
                        del lamesa.lista_lb[k]
                        lamesa.rln += 1
                        piece_respawn = 'lista_lb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_slb.items():
                    if e == destiny:
                        del lamesa.lista_slb[k]
                        lamesa.rln += 1
                        piece_respawn = 'lista_slb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_nb.items():
                    if e == destiny:
                        del lamesa.lista_nb[k]
                        lamesa.rnn += 1
                        piece_respawn = 'lista_nb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_snb.items():
                    if e == destiny:
                        del lamesa.lista_snb[k]
                        lamesa.rnn += 1
                        piece_respawn = 'lista_snb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_sb.items():
                    if e == destiny:
                        del lamesa.lista_sb[k]
                        lamesa.rsn += 1
                        piece_respawn = 'lista_sb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_ssb.items():
                    if e == destiny:
                        del lamesa.lista_ssb[k]
                        lamesa.rsn += 1
                        piece_respawn = 'lista_ssb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_gb.items():
                    if e == destiny:
                        del lamesa.lista_gb[k]
                        lamesa.rgn += 1
                        piece_respawn = 'lista_gb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_tb.items():
                    if e == destiny:
                        del lamesa.lista_tb[k]
                        lamesa.rtn += 1
                        piece_respawn = 'lista_tb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_stb.items():
                    if e == destiny:
                        del lamesa.lista_stb[k]
                        lamesa.rtn += 1
                        piece_respawn = 'lista_stb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_bb.items():
                    if e == destiny:
                        del lamesa.lista_bb[k]
                        lamesa.rbn += 1
                        piece_respawn = 'lista_bb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_sbb.items():
                    if e == destiny:
                        del lamesa.lista_sbb[k]
                        lamesa.rbn += 1
                        piece_respawn = 'lista_sbb['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
        else: # Blancas
            found = False
            while not found:
                for k, e in lamesa.lista_pn.items():
                    if e == destiny:
                        del lamesa.lista_pn[k]
                        lamesa.rpb += 1
                        piece_respawn = 'lista_pn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_spn.items():
                    if e == destiny:
                        del lamesa.lista_spn[k]
                        lamesa.rpb += 1
                        piece_respawn = 'lista_spn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_ln.items():
                    if e == destiny:
                        del lamesa.lista_ln[k]
                        lamesa.rlb += 1
                        piece_respawn = 'lista_ln['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_sln.items():
                    if e == destiny:
                        del lamesa.lista_sln[k]
                        lamesa.rlb += 1
                        piece_respawn = 'lista_sln['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_nn.items():
                    if e == destiny:
                        del lamesa.lista_nn[k]
                        lamesa.rnb += 1
                        piece_respawn = 'lista_nn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_snn.items():
                    if e == destiny:
                        del lamesa.lista_snn[k]
                        lamesa.rnb += 1
                        piece_respawn = 'lista_snn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_sn.items():
                    if e == destiny:
                        del lamesa.lista_sn[k]
                        lamesa.rsb += 1
                        piece_respawn = 'lista_sn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_ssn.items():
                    if e == destiny:
                        del lamesa.lista_ssn[k]
                        lamesa.rsb += 1
                        piece_respawn = 'lista_ssn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_gn.items():
                    if e == destiny:
                        del lamesa.lista_gn[k]
                        lamesa.rgb += 1
                        piece_respawn = 'lista_gn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_tn.items():
                    if e == destiny:
                        del lamesa.lista_tn[k]
                        lamesa.rtb += 1
                        piece_respawn = 'lista_tn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_stn.items():
                    if e == destiny:
                        del lamesa.lista_stn[k]
                        lamesa.rtb += 1
                        piece_respawn = 'lista_stn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_bn.items():
                    if e == destiny:
                        del lamesa.lista_bn[k]
                        lamesa.rbb += 1
                        piece_respawn = 'lista_bn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break
                if found:
                     break
                for k, e in lamesa.lista_sbn.items():
                    if e == destiny:
                        del lamesa.lista_sbn[k]
                        lamesa.rbb += 1
                        piece_respawn = 'lista_sbn['+(str)(k)+']=[lamesa'
                        piece_respawn+= '.coords_x["'+destiny_h[0]+'"],'
                        piece_respawn+= 'lamesa.coords_y["'+destiny_h[1]+'"]]'
                        found = True
                        break

    possible_moves = 0
    if piece_x == 0 and action != 2:
        if int(num_g) % 2 == 1: #Negras
            if kind == 'P':
                for k, pn in lamesa.lista_pn.items():
                    if destiny[0] == pn[0] and destiny[1] == pn[1]-71:
                        possible_moves += 1
                        move_to_add = (['lista_pn['+(str)(k)+']', [0, -71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_pn[k])
                        )
                        lamesa.lista_pn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_pn[k]
                            lamesa.lista_spn[k] = destiny
            if kind == 'L':
                for k, ln in lamesa.lista_ln.items():
                    if destiny[0] == ln[0] and destiny[1] < ln[1]:
                        if matrix.check_ln(matrix.get_hcoords(ln), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_ln['+(str)(k)+']',
                                           [0,destiny[1]-ln[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_ln[k])
                            )
                            lamesa.lista_ln[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_ln[k]
                                lamesa.lista_sln[k] = destiny
            if kind == 'N':
                for k, nn in lamesa.lista_nn.items():
                    if (destiny[0] == nn[0]+71 or
                            destiny[0] == nn[0]-71) and (destiny[1] ==
                            nn[1]-142):
                        possible_moves += 1
                        move_to_add = (['lista_nn['+(str)(k)+']',
                                       [destiny[0]-nn[0], destiny[1]-nn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_nn[k])
                        )
                        lamesa.lista_nn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_nn[k]
                            lamesa.lista_snn[k] = destiny
            if kind == 'S':
                for k, sn in lamesa.lista_sn.items():
                    if (destiny[0] <= sn[0]+71 and destiny[0] >= sn[0]-71 and
                            destiny[1] == sn[1]-71) or (
                             (destiny[0] == sn[0]+71 or
                             destiny[0] == sn[0]-71) and
                            destiny[1] == sn[1]+71):
                        possible_moves += 1
                        move_to_add = (['lista_sn['+(str)(k)+']',
                                       [destiny[0]-sn[0],destiny[1]-sn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_sn[k])
                        )
                        lamesa.lista_sn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_sn[k]
                            lamesa.lista_ssn[k] = destiny
            if kind == 'G':
                for k, gn in lamesa.lista_gn.items():
                    if (destiny[0] <= gn[0]+71 and destiny[0] >= gn[0]-71 and
                            destiny[1] == gn[1]-71) or ((destiny[0] ==
                            gn[0]+71 or destiny[0] == gn[0]-71)
                            and destiny[1] == gn[1]) or (destiny[0] ==
                            gn[0] and destiny[1] == gn[1]+71):
                        possible_moves += 1
                        move_to_add = (['lista_gn['+(str)(k)+']',
                                       [destiny[0]-gn[0],destiny[1]-gn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_gn[k])
                        )
                        lamesa.lista_gn[k] = destiny
                        matrix.fill(destiny_h)
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista_s'+mem+'n.items():\n'
                statem+= '    if (destiny[0] <= j[0]+71 and destiny[0] >='
                statem+= '            j[0]-71 and destiny[1] == j[1]-71) or ('
                statem+= '            (destiny[0] == j[0]+71 or destiny[0] =='
                statem+= '             j[0]-71) and destiny[1] == j[1]) or ('
                statem+= '             destiny[0] == j[0] and destiny[1] =='
                statem+= '             j[1]+71):\n'
                statem+= '        possible_moves += 1\n'
                statem+= '        move_to_add=["lista_s'+mem+'n["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista_s'+mem+'n[k]))\n'
                statem+= '        lamesa.lista_s'+mem+'n[k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista_tn.items():
                    if (destiny[0] == tn[0]) != (destiny[1] == tn[1]):
                        if matrix.check_t(matrix.get_hcoords(tn), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_tn['+(str)(k)+']',
                                           [destiny[0]-tn[0],
                                            destiny[1]-tn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_tn[k])
                            )
                            lamesa.lista_tn[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_tn[k]
                                lamesa.lista_stn[k] = destiny
            if kind == '+R':
                for k, stn in lamesa.lista_stn.items():
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
                            move_to_add = (['lista_stn['+(str)(k)+']',
                                           [destiny[0]-stn[0],
                                            destiny[1]-stn[1]],
                                            action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_stn[k])
                            )
                            lamesa.lista_stn[k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bn in lamesa.lista_bn.items():
                    if abs(destiny[0]-bn[0]) == abs(destiny[1]-bn[1]):
                        if matrix.check_b(matrix.get_hcoords(bn), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_bn['+(str)(k)+']',
                                           [destiny[0]-bn[0],destiny[1]-bn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_bn[k])
                            )
                            lamesa.lista_bn[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_bn[k]
                                lamesa.lista_sbn[k] = destiny
            if kind == '+B':
                for k, sbn in lamesa.lista_sbn.items():
                    if (abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) or (
                           destiny[0] <= sbn[0]+71 and destiny[0] >=
                           sbn[0]-71 and destiny[1] <= sbn[1]+71 and
                           destiny[1] >= sbn[1]-71):
                        if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbn),
                              destiny_h)) or not (abs(destiny[0]-sbn[0]) ==
                                abs(destiny[1]-sbn[1])):
                            possible_moves += 1
                            move_to_add = (['lista_sbn['+(str)(k)+']',
                                           [destiny[0]-sbn[0],
                                            destiny[1]-sbn[1]],
                                            action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_sbn[k])
                            )
                            lamesa.lista_sbn[k] = destiny
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
                for k, pb in lamesa.lista_pb.items():
                    if destiny[0] == pb[0] and destiny[1] == pb[1]+71:
                        possible_moves += 1
                        move_to_add = (['lista_pb['+(str)(k)+']',[0, 71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_pb[k])
                        )
                        lamesa.lista_pb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_pb[k]
                            lamesa.lista_spb[k] = destiny
            if kind == 'L':
                for k, lb in lamesa.lista_lb.items():
                    if destiny[0] == lb[0] and destiny[1] > lb[1]:
                        if matrix.check_lb(matrix.get_hcoords(lb), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_lb['+(str)(k)+']',
                                           [0,destiny[1]-lb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_lb[k])
                            )
                            lamesa.lista_lb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_lb[k]
                                lamesa.lista_slb[k] = destiny
            if kind == 'N':
                for k, nb in lamesa.lista_nb.items():
                    if (destiny[0] == nb[0]+71 or destiny[0] == nb[0]-71) and (
                               destiny[1] == nb[1]+142):
                        possible_moves += 1
                        move_to_add = (['lista_nb['+(str)(k)+']',
                                       [destiny[0]-nb[0],destiny[1]-nb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_nb[k])
                        )
                        lamesa.lista_nb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_nb[k]
                            lamesa.lista_snb[k] = destiny
            if kind == 'S':
                for k, sb in lamesa.lista_sb.items():
                    if (destiny[0] <= sb[0]+71 and destiny[0] >= sb[0]-71 and
                            destiny[1] == sb[1]+71) or (
                              (destiny[0] == sb[0]+71 or
                               destiny[0] == sb[0]-71) and
                              destiny[1] == sb[1]-71):
                        possible_moves += 1
                        move_to_add = (['lista_sb['+(str)(k)+']',
                                       [destiny[0]-sb[0],destiny[1]-sb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_sb[k])
                        )
                        lamesa.lista_sb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_sb[k]
                            lamesa.lista_ssb[k] = destiny
            if kind == 'G':
                for k, gb in lamesa.lista_gb.items():
                    if (destiny[0] <= gb[0]+71 and destiny[0] >= gb[0]-71 and
                             destiny[1] == gb[1]+71) or (
                              (destiny[0] == gb[0]+71 or
                                destiny[0] == gb[0]-71) and
                              destiny[1] == gb[1]) or (destiny[0] == gb[0] and
                              destiny[1] == gb[1]-71):
                        possible_moves += 1
                        move_to_add = (['lista_gb['+(str)(k)+']',
                                       [destiny[0]-gb[0],destiny[1]-gb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_gb[k])
                        )
                        lamesa.lista_gb[k] = destiny
                        matrix.fill(destiny_h)
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista_s'+mem+'b.items():\n'
                statem+= '    if (destiny[0] <= j[0]+71 and destiny[0] >='
                statem+= '            j[0]-71 and destiny[1] == j[1]+71) or ('
                statem+= '            (destiny[0] == j[0]+71 or destiny[0] =='
                statem+= '             j[0]-71) and destiny[1] == j[1]) or ('
                statem+= '             destiny[0] == j[0] and destiny[1] =='
                statem+= '             j[1]-71):\n'
                statem+= '        possible_moves += 1\n'
                statem+= '        move_to_add=["lista_s'+mem+'b["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista_s'+mem+'b[k]))\n'
                statem+= '        lamesa.lista_s'+mem+'b[k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista_tb.items():
                    if (destiny[0] == tb[0]) != (destiny[1] == tb[1]):
                        if matrix.check_t(matrix.get_hcoords(tb),destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_tb['+(str)(k)+']',
                                           [destiny[0]-tb[0],
                                            destiny[1]-tb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_tb[k])
                            )
                            lamesa.lista_tb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_tb[k]
                                lamesa.lista_stb[k] = destiny
            if kind == '+R':
                for k, stb in lamesa.lista_stb.items():
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
                            move_to_add = (['lista_stb['+(str)(k)+']',
                                           [destiny[0]-stb[0],
                                            destiny[1]-stb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_stb[k])
                            )
                            lamesa.lista_stb[k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bb in lamesa.lista_bb.items():
                    if abs(destiny[0]-bb[0]) == abs(destiny[1]-bb[1]):
                        if matrix.check_b(matrix.get_hcoords(bb), destiny_h):
                            possible_moves += 1
                            move_to_add = (['lista_bb['+(str)(k)+']',
                                           [destiny[0]-bb[0],
                                            destiny[1]-bb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_bb[k])
                            )
                            lamesa.lista_bb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_bb[k]
                                lamesa.lista_sbb[k] = destiny
            if kind == '+B':
                for k, sbb in lamesa.lista_sbb.items():
                    if (abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) or (
                           destiny[0] <= sbb[0]+71 and destiny[0] >=
                           sbb[0]-71 and destiny[1] <= sbb[1]+71 and
                           destiny[1] >= sbb[1]-71):
                        if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbb),
                              destiny_h)) or not (abs(destiny[0]-sbb[0]) ==
                                abs(destiny[1]-sbb[1])):
                            possible_moves += 1
                            move_to_add = (['lista_sbb['+(str)(k)+']',
                                           [destiny[0]-sbb[0],
                                            destiny[1]-sbb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_sbb[k])
                            )
                            lamesa.lista_sbb[k] = destiny
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
                for k, pn in lamesa.lista_pn.items():
                    if pn[0] == piece_x and pn[1] == piece_y:
                        move_to_add = (['lista_pn['+(str)(k)+']', [0,-71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_pn[k])
                        )
                        lamesa.lista_pn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_pn[k]
                            lamesa.lista_spn[k] = destiny
                        break
            if kind == 'L':
                for k, ln in lamesa.lista_ln.items():
                    if ln[0] == piece_x and ln[1] == piece_y:
                        if matrix.check_ln(matrix.get_hcoords(ln), destiny_h):
                            move_to_add = (['lista_ln['+(str)(k)+']',
                                           [0, destiny[1]-ln[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_ln[k])
                            )
                            lamesa.lista_ln[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_ln[k]
                                lamesa.lista_sln[k] = destiny
                            break
            if kind == 'N':
                for k, nn in lamesa.lista_nn.items():
                    if nn[0] == piece_x and nn[1] == piece_y:
                        move_to_add = (['lista_nn['+(str)(k)+']',
                                       [destiny[0]-nn[0],
                                        destiny[1]-nn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_nn[k])
                        )
                        lamesa.lista_nn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_nn[k]
                            lamesa.lista_snn[k] = destiny
                        break
            if kind == 'S':
                for k, sn in lamesa.lista_sn.items():
                    if sn[0] == piece_x and sn[1] == piece_y:
                        move_to_add = (['lista_sn['+(str)(k)+']',
                                       [destiny[0]-sn[0],
                                        destiny[1]-sn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_sn[k])
                        )
                        lamesa.lista_sn[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_sn[k]
                            lamesa.lista_ssn[k] = destiny
                        break
            if kind == 'G':
                for k, gn in lamesa.lista_gn.items():
                    if gn[0] == piece_x and gn[1] == piece_y:
                        move_to_add = (['lista_gn['+(str)(k)+']',
                                       [destiny[0]-gn[0], destiny[1]-gn[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_gn[k])
                        )
                        lamesa.lista_gn[k] = destiny
                        matrix.fill(destiny_h)
                        break
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista_s'+mem+'n.items():\n'
                statem+= '    if j[0] == piece_x and j[1] == piece_y:\n'
                statem+= '        move_to_add=["lista_s'+mem+'n["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista_s'+mem+'n[k]))\n'
                statem+= '        lamesa.lista_s'+mem+'n[k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista_tn.items():
                    if tn[0] == piece_x and tn[1] == piece_y:
                        if matrix.check_t(matrix.get_hcoords(tn), destiny_h):
                            move_to_add = (['lista_tn['+(str)(k)+']',
                                           [destiny[0]-tn[0],
                                            destiny[1]-tn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_tn[k])
                            )
                            lamesa.lista_tn[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_tn[k]
                                lamesa.lista_stn[k] = destiny
                            break
            if kind == '+R':
                for k, stn in lamesa.lista_stn.items():
                    if stn[0] == piece_x and stn[1] == piece_y:
                        if ((destiny[0] == stn[0]) != (destiny[1] == stn[1]
                            ) and matrix.check_t(matrix.get_hcoords(stn),
                              destiny_h)) or not ((destiny[0] == stn[0]) != (
                                destiny[1] == stn[1])):
                            move_to_add = (['lista_stn['+(str)(k)+']',
                                           [destiny[0]-stn[0],
                                            destiny[1]-stn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_stn[k])
                            )
                            lamesa.lista_stn[k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bn in lamesa.lista_bn.items():
                    if bn[0] == piece_x and bn[1] == piece_y:
                        if matrix.check_b(matrix.get_hcoords(bn),destiny_h):
                            move_to_add = (['lista_bn['+(str)(k)+']',
                                           [destiny[0]-bn[0],
                                            destiny[1]-bn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_bn[k])
                            )
                            lamesa.lista_bn[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_bn[k]
                                lamesa.lista_sbn[k] = destiny
                            break
            if kind == '+B':
                for k, sbn in lamesa.lista_sbn.items():
                    if sbn[0] == piece_x and sbn[1] == piece_y:
                        if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbn),
                                destiny_h)) or not (abs(destiny[0]-sbn[0]
                                ) == abs(destiny[1]-sbn[1])):
                            move_to_add = (['lista_sbn['+(str)(k)+']',
                                           [destiny[0]-sbn[0],
                                            destiny[1]-sbn[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_sbn[k])
                            )
                            lamesa.lista_sbn[k] = destiny
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
                for k, pb in lamesa.lista_pb.items():
                    if pb[0] == piece_x and pb[1] == piece_y:
                        move_to_add = (['lista_pb['+(str)(k)+']',[0,+71],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_pb[k])
                        )
                        lamesa.lista_pb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_pb[k]
                            lamesa.lista_spb[k] = destiny
                        break
            if kind == 'L':
                for k, lb in lamesa.lista_lb.items():
                    if lb[0] == piece_x and lb[1] == piece_y:
                        if matrix.check_lb(matrix.get_hcoords(lb), destiny_h):
                            move_to_add = (['lista_lb['+(str)(k)+']',
                                           [0, destiny[1]-lb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_lb[k])
                            )
                            lamesa.lista_lb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_lb[k]
                                lamesa.lista_slb[k] = destiny
                            break
            if kind == 'N':
                for k, nb in lamesa.lista_nb.items():
                    if nb[0] == piece_x and nb[1] == piece_y:
                        move_to_add = (['lista_nb['+(str)(k)+']',
                                       [destiny[0]-nb[0],
                                        destiny[1]-nb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_nb[k])
                        )
                        lamesa.lista_nb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_nb[k]
                            lamesa.lista_snb[k] = destiny
                        break
            if kind == 'S':
                for k, sb in lamesa.lista_sb.items():
                    if sb[0] == piece_x and sb[1] == piece_y:
                        move_to_add = (['lista_sb['+(str)(k)+']',
                                       [destiny[0]-sb[0],
                                        destiny[1]-sb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_sb[k])
                        )
                        lamesa.lista_sb[k] = destiny
                        matrix.fill(destiny_h)
                        if promoting:
                            del lamesa.lista_sb[k]
                            lamesa.lista_ssb[k] = destiny
                        break
            if kind == 'G':
                for k, gb in lamesa.lista_gb.items():
                    if gb[0] == piece_x and gb[1] == piece_y:
                        move_to_add = (['lista_gb['+(str)(k)+']',
                                       [destiny[0]-gb[0],
                                        destiny[1]-gb[1]],
                                       action, promoting, piece_respawn])
                        matrix.empty(
                                matrix.get_hcoords(lamesa.lista_gb[k])
                        )
                        lamesa.lista_gb[k] = destiny
                        matrix.fill(destiny_h)
                        break
            if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
                mem = kind[1].lower()
                statem = 'for k, j in lamesa.lista_s'+mem+'b.items():\n'
                statem+= '    if j[0] == piece_x and j[1] == piece_y:\n'
                statem+= '        move_to_add=["lista_s'+mem+'b["+(str)(k)+"]"'
                statem+= ',[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)
                statem+= ','+(str)(promoting)+',\''+piece_respawn+'\']\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista_s'+mem+'b[k]))\n'
                statem+= '        lamesa.lista_s'+mem+'b[k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n\t\t'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista_tb.items():
                    if tb[0] == piece_x and tb[1] == piece_y:
                        if matrix.check_t(matrix.get_hcoords(tb),destiny_h):
                            move_to_add = (['lista_tb['+(str)(k)+']',
                                           [destiny[0]-tb[0],
                                            destiny[1]-tb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_tb[k])
                            )
                            lamesa.lista_tb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_tb[k]
                                lamesa.lista_stb[k] = destiny
                            break
            if kind == '+R':
                for k, stb in lamesa.lista_stb.items():
                    if stb[0] == piece_x and stb[1] == piece_y:
                        if ((destiny[0] == stb[0]) != (destiny[1] == stb[1]
                            ) and matrix.check_t(matrix.get_hcoords(stb),
                              destiny_h)) or not ((destiny[0] == stb[0]) != (
                                destiny[1] == stb[1])):
                            move_to_add = (['lista_stb['+(str)(k)+']',
                                           [destiny[0]-stb[0],
                                            destiny[1]-stb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_stb[k])
                            )
                            lamesa.lista_stb[k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bb in lamesa.lista_bb.items():
                    if bb[0] == piece_x and bb[1] == piece_y:
                        if matrix.check_b(matrix.get_hcoords(bb),destiny_h):
                            move_to_add = (['lista_bb['+(str)(k)+']',
                                           [destiny[0]-bb[0],
                                            destiny[1]-bb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_bb[k])
                            )
                            lamesa.lista_bb[k] = destiny
                            matrix.fill(destiny_h)
                            if promoting:
                                del lamesa.lista_bb[k]
                                lamesa.lista_sbb[k] = destiny
                            break
            if kind == '+B':
                for k, sbb in lamesa.lista_sbb.items():
                    if sbb[0] == piece_x and sbb[1] == piece_y:
                        if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])
                            ) and matrix.check_b(matrix.get_hcoords(sbb),
                                destiny_h) == True) or not(abs(destiny[0]-sbb[0]
                                ) == abs(destiny[1]-sbb[1])):
                            move_to_add = (['lista_sbb['+(str)(k)+']',
                                           [destiny[0]-sbb[0],
                                            destiny[1]-sbb[1]],
                                           action, promoting, piece_respawn])
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista_sbb[k])
                            )
                            lamesa.lista_sbb[k] = destiny
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
                move_to_add = ([['pn',lamesa.cnt_pn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_pn[lamesa.cnt_pn] = destiny
                lamesa.cnt_pn += 1
                lamesa.rpn -= 1
            else:
                move_to_add = ([['pb',lamesa.cnt_pb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_pb[lamesa.cnt_pb] = destiny
                lamesa.cnt_pb += 1
                lamesa.rpb -= 1
        if kind == 'L':
            if player == 'n':
                move_to_add = ([['ln',lamesa.cnt_ln], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_ln[lamesa.cnt_ln] = destiny
                lamesa.cnt_ln += 1
                lamesa.rln -= 1
            else:
                move_to_add = ([['lb',lamesa.cnt_lb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_lb[lamesa.cnt_lb] = destiny
                lamesa.cnt_lb += 1
                lamesa.rlb -= 1
        if kind == 'N':
            if player == 'n':
                move_to_add = ([['nn',lamesa.cnt_nn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_nn[lamesa.cnt_nn] = destiny
                lamesa.cnt_nn += 1
                lamesa.rnn -= 1
            else:
                move_to_add = ([['nb',lamesa.cnt_nb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_nb[lamesa.cnt_nb] = destiny
                lamesa.cnt_nb += 1
                lamesa.rnb -= 1
        if kind == 'S':
            if player == 'n':
                move_to_add = ([['sn',lamesa.cnt_sn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_sn[lamesa.cnt_sn] = destiny
                lamesa.cnt_sn += 1
                lamesa.rsn -= 1
            else:
                move_to_add = ([['sb',lamesa.cnt_sb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_sb[lamesa.cnt_sb] = destiny
                lamesa.cnt_sb += 1
                lamesa.rsb -= 1
        if kind == 'G':
            if player == 'n':
                move_to_add = ([['gn',lamesa.cnt_gn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_gn[lamesa.cnt_gn] = destiny
                lamesa.cnt_gn += 1
                lamesa.rgn -= 1
            else:
                move_to_add = ([['gb',lamesa.cnt_gb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_gb[lamesa.cnt_gb] = destiny
                lamesa.cnt_gb += 1
                lamesa.rgb -= 1
        if kind == 'R':
            if player == 'n':
                move_to_add = ([['tn',lamesa.cnt_tn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_tn[lamesa.cnt_tn] = destiny
                lamesa.cnt_tn += 1
                lamesa.rtn -= 1
            else:
                move_to_add = ([['tb',lamesa.cnt_tb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_tb[lamesa.cnt_tb] = destiny
                lamesa.cnt_tb += 1
                lamesa.rtb -= 1
        if kind == 'B':
            if player == 'n':
                move_to_add = ([['bn',lamesa.cnt_bn], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_bn[lamesa.cnt_bn] = destiny
                lamesa.cnt_bn += 1
                lamesa.rbn -= 1
            else:
                move_to_add = ([['bb',lamesa.cnt_bb], destiny_h,
                                action, promoting, piece_respawn])
                lamesa.lista_bb[lamesa.cnt_bb] = destiny
                lamesa.cnt_bb += 1
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
        SCREEN.blit(sprites.pn_img, (res_n['p'][0]+mod, res_n['p'][1]))
    for i in xrange(0, lamesa.rpb):
        mod = i * 10
        SCREEN.blit(sprites.pb_img, (res_b['p'][0]+mod, res_b['p'][1]))
    for i in xrange(0, lamesa.rln):
        mod = i * 10
        SCREEN.blit(sprites.ln_img, (res_n['l'][0]+mod, res_n['l'][1]))
    for i in xrange(0, lamesa.rlb):
        mod = i * 10
        SCREEN.blit(sprites.lb_img, (res_b['l'][0]+mod, res_b['l'][1]))
    for i in xrange(0, lamesa.rnn):
        mod = i * 10
        SCREEN.blit(sprites.nn_img, (res_n['n'][0]+mod, res_n['n'][1]))
    for i in xrange(0, lamesa.rnb):
        mod = i * 10
        SCREEN.blit(sprites.nb_img, (res_b['n'][0]+mod, res_b['n'][1]))
    for i in xrange(0, lamesa.rsn):
        mod = i * 10
        SCREEN.blit(sprites.sn_img, (res_n['s'][0]+mod, res_n['s'][1]))
    for i in xrange(0, lamesa.rsb):
        mod = i * 10
        SCREEN.blit(sprites.sb_img, (res_b['s'][0]+mod, res_b['s'][1]))
    for i in xrange(0, lamesa.rgn):
        mod = i * 10
        SCREEN.blit(sprites.gn_img, (res_n['g'][0]+mod, res_n['g'][1]))
    for i in xrange(0, lamesa.rgb):
        mod = i * 10
        SCREEN.blit(sprites.gb_img, (res_b['g'][0]+mod, res_b['g'][1]))
    for i in xrange(0, lamesa.rtn):
        mod = i * 10
        SCREEN.blit(sprites.tn_img, (res_n['t'][0]+mod, res_n['t'][1]))
    for i in xrange(0, lamesa.rtb):
        mod = i * 10
        SCREEN.blit(sprites.tb_img, (res_b['t'][0]+mod, res_b['t'][1]))
    for i in xrange(0, lamesa.rbn):
        mod = i * 10
        SCREEN.blit(sprites.bn_img, (res_n['b'][0]+mod, res_n['b'][1]))
    for i in xrange(0, lamesa.rbb):
        mod = i * 10
        SCREEN.blit(sprites.bb_img, (res_b['b'][0]+mod, res_b['b'][1]))

    # *** This reads the current position of pieces to place them ***
    if lamesa.reverted == 1:
        comp_b = 2
        comp_n = 0
    else:
        comp_n = 2
        comp_b = 0
    for k, pn in lamesa.lista_pn.items():
        SCREEN.blit(sprites.pn_img, (pn[0]-comp_n, pn[1]-comp_n))
    for k, spn in lamesa.lista_spn.items():
        SCREEN.blit(sprites.spn_img, (spn[0]-comp_n, spn[1]-comp_n))
    for k, pb in lamesa.lista_pb.items():
        SCREEN.blit(sprites.pb_img, (pb[0]-comp_b, pb[1]-comp_b))
    for k, spb in lamesa.lista_spb.items():
        SCREEN.blit(sprites.spb_img, (spb[0]-comp_b, spb[1]-comp_b))
    for k, ln in lamesa.lista_ln.items():
        SCREEN.blit(sprites.ln_img, (ln[0]-comp_n, ln[1]-comp_n))
    for k, sln in lamesa.lista_sln.items():
        SCREEN.blit(sprites.sln_img, (sln[0]-comp_n, sln[1]-comp_n))
    for k, lb in lamesa.lista_lb.items():
        SCREEN.blit(sprites.lb_img, (lb[0]-comp_b, lb[1]-comp_b))
    for k, slb in lamesa.lista_slb.items():
        SCREEN.blit(sprites.slb_img, (slb[0]-comp_b, slb[1]-comp_b))
    for k, nn in lamesa.lista_nn.items():
        SCREEN.blit(sprites.nn_img, (nn[0]-comp_n, nn[1]-comp_n))
    for k, snn in lamesa.lista_snn.items():
        SCREEN.blit(sprites.snn_img, (snn[0]-comp_n, snn[1]-comp_n))
    for k, nb in lamesa.lista_nb.items():
        SCREEN.blit(sprites.nb_img, (nb[0]-comp_b, nb[1]-comp_b))
    for k, snb in lamesa.lista_snb.items():
        SCREEN.blit(sprites.snb_img, (snb[0]-comp_b, snb[1]-comp_b))
    for k, sn in lamesa.lista_sn.items():
        SCREEN.blit(sprites.sn_img, (sn[0]-comp_n, sn[1]-comp_n))
    for k, ssn in lamesa.lista_ssn.items():
        SCREEN.blit(sprites.ssn_img, (ssn[0]-comp_n, ssn[1]-comp_n))
    for k, sb in lamesa.lista_sb.items():
        SCREEN.blit(sprites.sb_img, (sb[0]-comp_b, sb[1]-comp_b))
    for k, ssb in lamesa.lista_ssb.items():
        SCREEN.blit(sprites.ssb_img, (ssb[0]-comp_b, ssb[1]-comp_b))
    for k, gn in lamesa.lista_gn.items():
        SCREEN.blit(sprites.gn_img, (gn[0]-comp_n, gn[1]-comp_n))
    for k, gb in lamesa.lista_gb.items():
        SCREEN.blit(sprites.gb_img, (gb[0]-comp_b, gb[1]-comp_b))
    for k, tn in lamesa.lista_tn.items():
        SCREEN.blit(sprites.tn_img, (tn[0]-comp_n, tn[1]-comp_n))
    for k, stn in lamesa.lista_stn.items():
        SCREEN.blit(sprites.stn_img, (stn[0]-comp_n, stn[1]-comp_n))
    for k, tb in lamesa.lista_tb.items():
        SCREEN.blit(sprites.tb_img, (tb[0]-comp_b, tb[1]-comp_b))
    for k, stb in lamesa.lista_stb.items():
        SCREEN.blit(sprites.stb_img, (stb[0]-comp_b, stb[1]-comp_b))
    for k, bn in lamesa.lista_bn.items():
        SCREEN.blit(sprites.bn_img, (bn[0]-comp_n, bn[1]-comp_n))
    for k, sbn in lamesa.lista_sbn.items():
        SCREEN.blit(sprites.sbn_img, (sbn[0]-comp_n, sbn[1]-comp_n))
    for k, bb in lamesa.lista_bb.items():
        SCREEN.blit(sprites.bb_img, (bb[0]-comp_b, bb[1]-comp_b))
    for k, sbb in lamesa.lista_sbb.items():
        SCREEN.blit(sprites.sbb_img, (sbb[0]-comp_b, sbb[1]-comp_b))
    SCREEN.blit(sprites.kn_img,
                (lamesa.rey_n[0]-comp_n, lamesa.rey_n[1]-comp_n))
    SCREEN.blit(sprites.kb_img,
                (lamesa.rey_b[0]-comp_b, lamesa.rey_b[1]-comp_b))

#    reloj.tick(10)
    pygame.display.flip()
# una mas eficiente, que no actualiza la pantalla entera. busca sobre ésta:
# pygame.display.update()
