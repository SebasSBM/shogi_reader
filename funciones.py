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
    This file contains functions defined for shogi_reader
"""
import pygame
from globales import *
from globalvars import *


# ******* TABLERO ********

def redraw():
    r = 235
    g = 220
    b = 180
    bg = int(r), int(g), int(b)

    SCREEN.fill(bg)
    pygame.draw.rect(SCREEN, (82,64,4), (20, 20, 230, 284))
    pygame.draw.rect(SCREEN, (82,64,4), (930, 375, 230, 284))

    #Verticals
    pygame.draw.line(SCREEN, (0,0,0), (268,20), (268,659))
    pygame.draw.line(SCREEN, (0,0,0), (339,20), (339,659))
    pygame.draw.line(SCREEN, (0,0,0), (410,20), (410,659))
    pygame.draw.line(SCREEN, (0,0,0), (481,20), (481,659))
    pygame.draw.line(SCREEN, (0,0,0), (552,20), (552,659))
    pygame.draw.line(SCREEN, (0,0,0), (623,20), (623,659))
    pygame.draw.line(SCREEN, (0,0,0), (694,20), (694,659))
    pygame.draw.line(SCREEN, (0,0,0), (765,20), (765,659))
    pygame.draw.line(SCREEN, (0,0,0), (836,20), (836,659))
    pygame.draw.line(SCREEN, (0,0,0), (907,20), (907,659))

    #Horizontals
    pygame.draw.line(SCREEN, (0,0,0), (268,20), (907,20))
    pygame.draw.line(SCREEN, (0,0,0), (268,91), (907,91))
    pygame.draw.line(SCREEN, (0,0,0), (268,162), (907,162))
    pygame.draw.line(SCREEN, (0,0,0), (268,233), (907,233))
    pygame.draw.line(SCREEN, (0,0,0), (268,304), (907,304))
    pygame.draw.line(SCREEN, (0,0,0), (268,375), (907,375))
    pygame.draw.line(SCREEN, (0,0,0), (268,446), (907,446))
    pygame.draw.line(SCREEN, (0,0,0), (268,517), (907,517))
    pygame.draw.line(SCREEN, (0,0,0), (268,588), (907,588))
    pygame.draw.line(SCREEN, (0,0,0), (268,659), (907,659))


def move_forward():
    global pos, history
    if pos < len(history):
        if history[pos].action == 2:
            lamesa.lista[history[pos].piece_kind][history[pos].piece_id]=[
                         lamesa.coords_x[history[pos].coords[0]],
                         lamesa.coords_y[history[pos].coords[1]],
            ]
            lamesa.r[history[pos].piece_kind] -= 1
        else:
            lamesa.lista[history[pos].piece_kind][history[pos].piece_id][0]+=(
                history[pos].coords[0] * lamesa.reverted
            )
            lamesa.lista[history[pos].piece_kind][history[pos].piece_id][1]+=(
                history[pos].coords[1] * lamesa.reverted
            )

            if history[pos].promoting:
                hold_it = lamesa.lista[history[pos].piece_kind][
                                       history[pos].piece_id]
                hold_kind = history[pos].piece_kind
                hold_id = history[pos].piece_id
                del lamesa.lista[history[pos].piece_kind][
                                 history[pos].piece_id]
                lamesa.lista[hold_kind+2][hold_id] = hold_it


        #Piece captured that has to be respawn backwards
        if history[pos].respawn_kind is not None:
            thekind = history[pos].respawn_kind
            piece = history[pos].respawn_id
            PROMOTED_KINDS = [SPN,SPB,SLN,SLB,SNN,SNB,SSN,SSB,STN,STB,SBN,SBB]
            finalkind = thekind
            if thekind in PROMOTED_KINDS:
                finalkind -= 2
            if thekind % 2 == 0:
                finalkind += 1
            else:
                finalkind -=1

            del lamesa.lista[thekind][piece]
            lamesa.r[finalkind] += 1
        pos += 1
        previous_highlight(pos)


def previous_highlight(cursor=pos):
    global history, SCREEN
    if history[cursor-1].action != 2:
        if cursor > 0:
            thekind = history[cursor-1].piece_kind
            thepiece = history[cursor-1].piece_id
            if history[cursor-1].promoting:
                thekind += 2
            coords = lamesa.lista[thekind][thepiece]

            drawcoords = [coords[0]-history[cursor-1].coords[0]*lamesa.reverted,
                          coords[1]-history[cursor-1].coords[1]*lamesa.reverted]
            pygame.draw.rect(SCREEN, (255,0,0),
                             (drawcoords[0], drawcoords[1], 70, 70))
            drawcoords = [coords[0],coords[1]]
            pygame.draw.rect(SCREEN, (0,255,0),
                             (drawcoords[0], drawcoords[1], 70, 70))
    elif cursor > 0:
        pygame.draw.rect(SCREEN, (0,255,0),(
                          lamesa.coords_x[history[cursor-1].coords[0]],
                          lamesa.coords_y[history[cursor-1].coords[1]],70, 70))


def move_back():
    global pos, history
    if pos > 0:
        pos -= 1
        if history[pos].action == 2:
            del lamesa.lista[history[pos].piece_kind][history[pos].piece_id]
            lamesa.r[history[pos].piece_kind] += 1
        else:
            thekind = history[pos].piece_kind
            thepiece = history[pos].piece_id
            thecoords = history[pos].coords
            if history[pos].promoting:
                promo_coords = lamesa.lista[thekind+2][thepiece]
                lamesa.lista[thekind][thepiece] = [
                                     promo_coords[0],
                                     promo_coords[1]
                ]
                del lamesa.lista[thekind+2][thepiece]
            lamesa.lista[thekind][thepiece][0] -= (thecoords[0]
                                                   * lamesa.reverted)
            lamesa.lista[thekind][thepiece][1] -= (thecoords[1]
                                                   * lamesa.reverted)
        if history[pos].respawn_kind is not None:
            PROMOTED_KINDS = [SPN,SPB,SLN,SLB,SNN,SNB,SSN,SSB,STN,STB,SBN,SBB]
            thekind = history[pos].respawn_kind
            piece = history[pos].respawn_id
            thecoords = history[pos].respawn_coords
            finalkind = thekind
            if thekind in PROMOTED_KINDS:
                finalkind -= 2
            if thekind % 2 == 0:
                finalkind += 1
            else:
                finalkind -=1
            # Respawn piece
            lamesa.lista[thekind][piece]=[
                           lamesa.coords_x[thecoords[0]],
                           lamesa.coords_y[thecoords[1]]
            ]
            lamesa.r[finalkind] -= 1
        previous_highlight(pos)

def show_names():
    # *** Player names ***
    if lamesa.reverted != 1:
        cad1 = game_data.sente
        cad2 = game_data.gote
    else:
        cad1 = game_data.gote
        cad2 = game_data.sente
        
    label1 = FONT.render(cad1, 1, (0,0,0))
    SCREEN.blit(label1, (20,304))
    label2 = FONT.render(cad2, 1, (0,0,0))
    SCREEN.blit(label2, (930,355))

def get_pos():
    return pos
