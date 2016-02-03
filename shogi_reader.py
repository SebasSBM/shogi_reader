#!/usr/bin/env python
# coding: utf-8

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

import pygame
import sys
import re

pygame.init()
from pygame.locals import *

from managers import MatrixManager, SpritesManager, Move
from globales import *
from globalvars import history, lamesa, partida, rawgame, game_data
from funciones import redraw

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
matrix = MatrixManager()

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

    # Create respawn data for captured piece
    if action == 1:
        PROMOTED_KINDS = [SPN,SPB,SLN,SLB,SNN,SNB,SSN,SSB,STN,STB,SBN,SBB]
        found = False
        while not found:
            for sho in xrange(0,27):
                for k, e in lamesa.lista[sho].items():
                    if e == destiny:
                        del lamesa.lista[sho][k]
                        fres = (sho if not sho in
                                 PROMOTED_KINDS else sho - 2)
                        fres += -1 if sente else 1
                        lamesa.r[fres] += 1
                        piece_respawn[0] = sho
                        piece_respawn[1] = k
                        piece_respawn[2] = [destiny_h[0], destiny_h[1]]
                        found = True
                        break

    possible_moves = 0
    # Case: starting coords of piece not provided
    if piece_x == 0 and action != 2:
        if sente: #Negras
            if kind == 'P':
                for k, pn in lamesa.lista[PN].items():
                    if destiny[0] == pn[0] and destiny[1] == pn[1]-71:
                        possible_moves += 1
                        move_to_add = Move(PN, k, [0,-71], action,
                                         promoting, piece_respawn)
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
                        if matrix.check(LN, matrix.get_hcoords(ln), destiny_h):
                            possible_moves += 1
                            move_to_add = Move(LN, k, [0,destiny[1]-ln[1]],
                                          action, promoting, piece_respawn)
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
                        move_to_add = Move(NN, k, [destiny[0]-nn[0],
                                           destiny[1]-nn[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(SN, k, [destiny[0]-sn[0],
                                           destiny[1]-sn[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(GN, k, [destiny[0]-gn[0],
                                           destiny[1]-gn[1]], action,
                                           promoting, piece_respawn)
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
                statem+= '        move_to_add = Move(S'+mem+'N, k,'
                statem+= '[destiny[0]-j[0],destiny[1]-j[1]],'+str(action)+','
                statem+=  str(promoting)+',piece_respawn)\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'N][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'N][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista[TN].items():
                    if (destiny[0] == tn[0]) != (destiny[1] == tn[1]):
                        if matrix.check(TN, matrix.get_hcoords(tn), destiny_h):
                            possible_moves += 1
                            move_to_add = Move(TN, k, [destiny[0]-tn[0],
                                               destiny[1]-tn[1]], action,
                                               promoting, piece_respawn)
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
                                  stn[1]) and matrix.check(STN,
                                        matrix.get_hcoords(stn),
                                        destiny_h)) or not((destiny[0] ==
                                   stn[0]) != (destiny[1] == stn[1])):
                            possible_moves += 1
                            move_to_add = Move(STN, k, [destiny[0]-stn[0],
                                               destiny[1]-stn[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STN][k])
                            )
                            lamesa.lista[STN][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bn in lamesa.lista[BN].items():
                    if abs(destiny[0]-bn[0]) == abs(destiny[1]-bn[1]):
                        if matrix.check(BN, matrix.get_hcoords(bn), destiny_h):
                            possible_moves += 1
                            move_to_add = Move(BN, k, [destiny[0]-bn[0],
                                               destiny[1]-bn[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(SBN, matrix.get_hcoords(sbn),
                              destiny_h)) or not (abs(destiny[0]-sbn[0]) ==
                                abs(destiny[1]-sbn[1])):
                            possible_moves += 1
                            move_to_add = Move(SBN, k, [destiny[0]-sbn[0],
                                               destiny[1]-sbn[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBN][k])
                            )
                            lamesa.lista[SBN][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'K':
                if (destiny[0] <= lamesa.lista[KN][1][0]+71 and
                        destiny[0] >= lamesa.lista[KN][1][0]-71 and
                        destiny[1] <= lamesa.lista[KN][1][1]+71 and
                        destiny[1] >= lamesa.lista[KN][1][1]-71):
                    move_to_add = Move(KN, 1,
                                       [destiny[0]-lamesa.lista[KN][1][0],
                                       destiny[1]-lamesa.lista[KN][1][1]],
                                       action, promoting, piece_respawn)
                    matrix.empty(matrix.get_hcoords(lamesa.lista[KN][1]))
                    lamesa.lista[KN][1] = destiny
                    matrix.fill(destiny_h)
        else: #Blancas
            if kind == 'P':
                for k, pb in lamesa.lista[PB].items():
                    if destiny[0] == pb[0] and destiny[1] == pb[1]+71:
                        possible_moves += 1
                        move_to_add = Move(PB, k, [0, 71], action,
                                           promoting, piece_respawn)
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
                        if matrix.check(LB, matrix.get_hcoords(lb), destiny_h):
                            possible_moves += 1
                            move_to_add = Move(LB, k, [0, destiny[1]-lb[1]],
                                               action, promoting, piece_respawn)
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
                        move_to_add = Move(NB, k, [destiny[0]-nb[0],
                                           destiny[1]-nb[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(SB, k, [destiny[0]-sb[0],
                                           destiny[1]-sb[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(GB, k, [destiny[0]-gb[0],
                                           destiny[1]-gb[1]], action,
                                           promoting, piece_respawn)
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
                statem+= '        move_to_add = Move(S'+mem+'B, k,'
                statem+= '[destiny[0]-j[0],destiny[1]-j[1]],'+str(action)+','
                statem+=  str(promoting)+',piece_respawn)\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'B][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'B][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista[TB].items():
                    if (destiny[0] == tb[0]) != (destiny[1] == tb[1]):
                        if matrix.check(TB, matrix.get_hcoords(tb),destiny_h):
                            possible_moves += 1
                            move_to_add = Move(TB, k, [destiny[0]-tb[0],
                                               destiny[1]-tb[1]], action,
                                               promoting, piece_respawn)
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
                                  stb[1]) and matrix.check(STB,
                                        matrix.get_hcoords(stb),
                                        destiny_h)) or not((destiny[0] ==
                                   stb[0]) != (destiny[1] == stb[1])):
                            possible_moves += 1
                            move_to_add = Move(STB, k, [destiny[0]-stb[0],
                                               destiny[1]-stb[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STB][k])
                            )
                            lamesa.lista[STB][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'B':
                for k, bb in lamesa.lista[BB].items():
                    if abs(destiny[0]-bb[0]) == abs(destiny[1]-bb[1]):
                        if matrix.check(BB, matrix.get_hcoords(bb), destiny_h):
                            possible_moves += 1
                            move_to_add = Move(BB, k, [destiny[0]-bb[0],
                                               destiny[1]-bb[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(SBB, matrix.get_hcoords(sbb),
                              destiny_h)) or not (abs(destiny[0]-sbb[0]) ==
                                abs(destiny[1]-sbb[1])):
                            possible_moves += 1
                            move_to_add = Move(SBB, k, [destiny[0]-sbb[0],
                                               destiny[1]-sbb[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBB][k])
                            )
                            lamesa.lista[SBB][k] = destiny
                            matrix.fill(destiny_h)
            if kind == 'K':
                if (destiny[0] <= lamesa.lista[KB][1][0]+71 and
                        destiny[0] >= lamesa.lista[KB][1][0]-71 and
                        destiny[1] <= lamesa.lista[KB][1][1]+71 and
                        destiny[1] >= lamesa.lista[KB][1][1]-71):
                    move_to_add = Move(KB, 1,
                                       [destiny[0]-lamesa.lista[KB][1][0],
                                       destiny[1]-lamesa.lista[KB][1][1]],
                                       action, promoting, piece_respawn)
                    matrix.empty(matrix.get_hcoords(lamesa.lista[KB][1]))
                    lamesa.lista[KB][1] = destiny
                    matrix.fill(destiny_h)
    # Case: initial piece coords provided AND it's not a drop
    elif action != 2:
        if sente: #Negras
            if kind == 'P':
                for k, pn in lamesa.lista[PN].items():
                    if pn[0] == piece_x and pn[1] == piece_y:
                        move_to_add = Move(PN, k, [0,-71], action,
                                           promoting, piece_respawn)
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
                        if matrix.check(LN, matrix.get_hcoords(ln), destiny_h):
                            move_to_add = Move(LN, k, [0,destiny[1]-ln[1]],
                                               action, promoting, piece_respawn)
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
                        move_to_add = Move(NN, k, [destiny[0]-nn[0],
                                           destiny[1]-nn[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(SN, k, [destiny[0]-sn[0],
                                           destiny[1]-sn[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(GN, k, [destiny[0]-gn[0],
                                           destiny[1]-gn[1]], action,
                                           promoting, piece_respawn)
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
                statem+= '        move_to_add = Move(S'+mem+'N, k,'
                statem+= '[destiny[0]-j[0],destiny[1]-j[1]],'+str(action)+','
                statem+=  str(promoting)+',piece_respawn)\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'N][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'N][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tn in lamesa.lista[TN].items():
                    if tn[0] == piece_x and tn[1] == piece_y:
                        if matrix.check(TN, matrix.get_hcoords(tn), destiny_h):
                            move_to_add = Move(TN, k, [destiny[0]-tn[0],
                                               destiny[1]-tn[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(STN, matrix.get_hcoords(stn),
                              destiny_h)) or not ((destiny[0] == stn[0]) != (
                                destiny[1] == stn[1])):
                            move_to_add = Move(STN, k, [destiny[0]-stn[0],
                                               destiny[1]-stn[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STN][k])
                            )
                            lamesa.lista[STN][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bn in lamesa.lista[BN].items():
                    if bn[0] == piece_x and bn[1] == piece_y:
                        if matrix.check(BN, matrix.get_hcoords(bn),destiny_h):
                            move_to_add = Move(BN, k, [destiny[0]-bn[0],
                                               destiny[1]-bn[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(SBN, matrix.get_hcoords(sbn),
                                destiny_h)) or not (abs(destiny[0]-sbn[0]
                                ) == abs(destiny[1]-sbn[1])):
                            move_to_add = Move(SBN, k, [destiny[0]-sbn[0],
                                               destiny[1]-sbn[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBN][k])
                            )
                            lamesa.lista[SBN][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'K':
                if (lamesa.lista[KN][1][0] == piece_x and
                          lamesa.lista[KN][1][1] == piece_y):
                    move_to_add = Move(KN, 1,
                                       [destiny[0]-lamesa.lista[KN][1][0],
                                       destiny[1]-lamesa.lista[KN][1][1]],
                                       action, promoting, piece_respawn)
                    matrix.empty(matrix.get_hcoords(lamesa.lista[KN][1]))
                    lamesa.lista[KN][1] = destiny
                    matrix.fill(destiny_h)
        else: # Blancas
            if kind == 'P':
                for k, pb in lamesa.lista[PB].items():
                    if pb[0] == piece_x and pb[1] == piece_y:
                        move_to_add = Move(PB, k, [0,71], action,
                                           promoting, piece_respawn)
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
                        if matrix.check(LB, matrix.get_hcoords(lb), destiny_h):
                            move_to_add = Move(LB, k, [0,destiny[1]-lb[1]],
                                               action, promoting, piece_respawn)
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
                        move_to_add = Move(NB, k, [destiny[0]-nb[0],
                                           destiny[1]-nb[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(SB, k, [destiny[0]-sb[0],
                                           destiny[1]-sb[1]], action,
                                           promoting, piece_respawn)
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
                        move_to_add = Move(GB, k, [destiny[0]-gb[0],
                                           destiny[1]-gb[1]], action,
                                           promoting, piece_respawn)
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
                statem+= '        move_to_add = Move(S'+mem+'B, k,'
                statem+= '[destiny[0]-j[0],destiny[1]-j[1]],'+str(action)+','
                statem+=  str(promoting)+',piece_respawn)\n'
                statem+= '        matrix.empty(matrix.get_hcoords('
                statem+= 'lamesa.lista[S'+mem+'B][k]))\n'
                statem+= '        lamesa.lista[S'+mem+'B][k] = destiny\n'
                statem+= '        matrix.fill(destiny_h)\n\t\t'
                statem+= '        break'
                exec statem
            if kind == 'R':
                for k, tb in lamesa.lista[TB].items():
                    if tb[0] == piece_x and tb[1] == piece_y:
                        if matrix.check(TB, matrix.get_hcoords(tb),destiny_h):
                            move_to_add = Move(TB, k, [destiny[0]-tb[0],
                                               destiny[1]-tb[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(STB, matrix.get_hcoords(stb),
                              destiny_h)) or not ((destiny[0] == stb[0]) != (
                                destiny[1] == stb[1])):
                            move_to_add = Move(STB, k, [destiny[0]-stb[0],
                                               destiny[1]-stb[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[STB][k])
                            )
                            lamesa.lista[STB][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'B':
                for k, bb in lamesa.lista[BB].items():
                    if bb[0] == piece_x and bb[1] == piece_y:
                        if matrix.check(BB, matrix.get_hcoords(bb),destiny_h):
                            move_to_add = Move(BB, k, [destiny[0]-bb[0],
                                               destiny[1]-bb[1]], action,
                                               promoting, piece_respawn)
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
                            ) and matrix.check(SBB, matrix.get_hcoords(sbb),
                                destiny_h) == True) or not(abs(destiny[0]-sbb[0]
                                ) == abs(destiny[1]-sbb[1])):
                            move_to_add = Move(SBB, k, [destiny[0]-sbb[0],
                                               destiny[1]-sbb[1]], action,
                                               promoting, piece_respawn)
                            matrix.empty(
                                    matrix.get_hcoords(lamesa.lista[SBB][k])
                            )
                            lamesa.lista[SBB][k] = destiny
                            matrix.fill(destiny_h)
                            break
            if kind == 'K':
                if (lamesa.lista[KB][1][0] == piece_x and
                          lamesa.lista[KB][1][1] == piece_y):
                    move_to_add = Move(KB, 1,
                                       [destiny[0]-lamesa.lista[KB][1][0],
                                       destiny[1]-lamesa.lista[KB][1][1]],
                                       action, promoting, piece_respawn)
                    matrix.empty(matrix.get_hcoords(lamesa.lista[KB][1]))
                    lamesa.lista[KB][1] = destiny
                    matrix.fill(destiny_h)
    else: # Action=2 (piece drop)
        NORMAL_KINDS = [PN,PB,LN,LB,NN,NB,SN,SB,GN,GB,TN,TB,BN,BB]
        CONVERT_KIND = { 'Pn': PN, 'Pb': PB,
                         'Ln': LN, 'Lb': LB,
                         'Nn': NN, 'Nb': NB,
                         'Sn': SN, 'Sb': SB,
                         'Gn': GN, 'Gb': GB,
                         'Rn': TN, 'Rb': TB,
                         'Bn': BN, 'Bb': BB }
        if sente: #Negras
            player = 'n'
        else:
            player = 'b'
        dry = CONVERT_KIND[kind+player]
        move_to_add = Move(dry, lamesa.cnt[dry], destiny_h,
                           action, promoting, piece_respawn)
        lamesa.lista[dry][lamesa.cnt[dry]] = destiny
        lamesa.cnt[dry] += 1
        lamesa.r[dry] -= 1

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
        
# *** From here, the history array is full of Move instances.
# *** So we restart the board(lamesa) to start drawing with pygame
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
