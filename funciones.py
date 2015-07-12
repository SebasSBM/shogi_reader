#!/usr/bin/env python
# * coding: utf-8 *

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
    output = ''
    if pos < len(history):
        if history[pos][2] == 2:
            #In this case,
            # history[pos] structure -> [[kind_of_piece,counter_to_assign_id], destiny_coords, action, promoting, piece_respawn]
            statem = 'lamesa.lista_'+history[pos][0][0]+'['+(str)(history[pos][0][1])+']=['+(str)(lamesa.coords_x[history[pos][1][0]])+','+(str)(lamesa.coords_y[history[pos][1][1]])+']'
            exec statem
            output = 'lamesa.r'+history[pos][0][0]+' -= 1'
        else:
            # Standard case,
            # history[pos] structure -> [code_statement_to_select_piece, coords_sum, action, promoting, piece_respawn]
            statem = 'lamesa.'+history[pos][0]+'[0]+='+(str)(history[pos][1][0]*lamesa.reverted)
            exec statem
            statem = 'lamesa.'+history[pos][0]+'[1]+='+(str)(history[pos][1][1]*lamesa.reverted)
            exec statem
            if history[pos][3] == True: #Handle piece_promotion==True
                #TODO Simplify this task avoiding the regexp abuse
                prueba = re.match(r'^.*\[(.*)\]$', history[pos][0])
                statem = 'prueba2=lamesa.'+history[pos][0]
                exec statem
                statem = 'del lamesa.'+history[pos][0]
                exec statem
                prueba4 = re.match(r'^.*_(.*)\[.*\]$', history[pos][0])
                statem = 'lamesa.lista_s'+prueba4.group(1)+'['+prueba.group(1)+']=['+(str)(prueba2[0])+','+(str)(prueba2[1])+']'
                exec statem
        if history[pos][4] != '':#Piece captured that has to be respawn backwards
            # TODO Avoid regexp abuse
            frag = re.match(r'^(lista_(.*)\[.*\])=\[.*,.*\]$', history[pos][4])
            theobj = frag.group(1)
            piece = frag.group(2)
            if len(piece) == 3:
                piece = piece[1:]
            if piece[-1] == 'b':
                piece = piece[:-1]+'n'
            else:
                piece = piece[:-1]+'b'
            statem = 'del lamesa.'+theobj
            exec statem
            output = 'lamesa.r'+piece+' += 1'
        pos += 1
        previous_highlight(pos)
    return output

def previous_highlight(cursor=pos):
    global history, SCREEN
    if history[cursor-1][2] != 2:
        if cursor > 0:
            obj = history[cursor-1][0]
            if history[cursor-1][3] == True:
                frag = re.match(r'^lista_(.*\[.*\])$', obj)
                obj = 'lista_s'+frag.group(1)
            statem = 'coords=lamesa.'+obj
            exec statem
            drawcoords = [coords[0]-history[cursor-1][1][0]*lamesa.reverted,coords[1]-history[cursor-1][1][1]*lamesa.reverted]
            pygame.draw.rect(SCREEN, (255,0,0), (drawcoords[0], drawcoords[1], 70, 70))
            drawcoords = [coords[0],coords[1]]
            pygame.draw.rect(SCREEN, (0,255,0), (drawcoords[0], drawcoords[1], 70, 70))
    elif cursor > 0:
        pygame.draw.rect(SCREEN, (0,255,0), (lamesa.coords_x[history[cursor-1][1][0]], lamesa.coords_y[history[cursor-1][1][1]], 70, 70))

            
    
def move_back():
    global pos, history
    output = ''
    if pos > 0:
        pos -= 1
        if history[pos][2] == 2:
            statem = 'del lamesa.lista_'+history[pos][0][0]+'['+(str)(history[pos][0][1])+']'
            exec statem
            output = 'lamesa.r'+history[pos][0][0]+' += 1'
        else:
            if history[pos][3] == True:
                #TODO Avoid regexp abuse
                prueba = re.match(r'^.*\[(.*)\]$', history[pos][0])
                prueba4 = re.match(r'^.*_(.*)\[.*\]$', history[pos][0])
                statem = 'prueba2=lamesa.lista_s'+prueba4.group(1)+'['+prueba.group(1)+']'
                exec statem
                statem = 'lamesa.'+history[pos][0]+'=['+(str)(prueba2[0])+','+(str)(prueba2[1])+']'
                exec statem
                statem = 'del lamesa.lista_s'+prueba4.group(1)+'['+prueba.group(1)+']'
                exec statem
            statem = 'lamesa.'+history[pos][0]+'[0]-='+(str)(history[pos][1][0]*lamesa.reverted)
            exec statem
            statem = 'lamesa.'+history[pos][0]+'[1]-='+(str)(history[pos][1][1]*lamesa.reverted)
            exec statem
        if history[pos][4] != '':
            frag = re.match(r'^lista_(.*)\[.*\]=\[.*,.*\]$', history[pos][4])
            piece = frag.group(1)
            if len(piece) == 3:
                piece = piece[1:]
            if piece[-1] == 'b':
                piece = piece[:-1]+'n'
            else:
                piece = piece[:-1]+'b'
            exec 'lamesa.'+history[pos][4]
            output = 'lamesa.r'+piece+' -= 1'
        previous_highlight(pos)
    return output

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
