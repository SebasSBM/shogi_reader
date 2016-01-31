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
    This file contains the classes defined for shogi_reader
"""
import pygame, re, tkMessageBox
from globales import MAINPATH, SCREEN, FONT

from globales import (PN, PB, SPN, SPB, LN, LB, SLN, SLB, NN, NB, SNN,
                      SNB, SN, SB, SSN, SSB, TN, TB, STN, STB, BN, BB,
                      SBN, SBB, GN, GB, KN, KB)


class Move:
    def __init__(self, piece_kind, piece_id, coords,
                 action, promoting, piece_respawn=None):
        self.piece_kind = piece_kind
        self.piece_id = piece_id
        self.coords = coords
        self.action = action
        self.promoting = promoting
        self.respawn_kind = None
        self.respawn_id = None
        self.respawn_coords = None
        if piece_respawn is not None:
            self.respawn_kind = piece_respawn[0]
            self.respawn_id = piece_respawn[1]
            self.respawn_coords = piece_respawn[2]

class coords_manager:
    def __init__(self):
        # Pieces arrays
        self.lista = [{},{}]
        self.cnt = []
        self.r = []
        for i in xrange(0,26):
            self.lista.append({})
            self.cnt.append([])
            self.r.append([])

        self.reverted = 1 #1 OR -1
        self.coords_ax = {
            '1': 837,
            '2': 766,
            '3': 695,
            '4': 624,
            '5': 553,
            '6': 482,
            '7': 411,
            '8': 340,
            '9': 269
        }
        self.coords_ay = {
            'i': 589,
            'h': 518,
            'g': 447,
            'f': 376,
            'e': 305,
            'd': 234,
            'c': 163,
            'b': 92,
            'a': 21
        }
        self.coords_bx = {
            '1': 269,
            '2': 340,
            '3': 411,
            '4': 482,
            '5': 553,
            '6': 624,
            '7': 695,
            '8': 766,
            '9': 837
        }
        self.coords_by = {
            'a': 589,
            'b': 518,
            'c': 447,
            'd': 376,
            'e': 305,
            'f': 234,
            'g': 163,
            'h': 92,
            'i': 21
        }
        self.coords_x = None
        self.coords_y = None
        self.update()
        self.begin()

    def begin(self):
        self.lista[PN] = {1:[self.coords_x['1'],self.coords_y['g']],
                          2:[self.coords_x['2'],self.coords_y['g']],
                          3:[self.coords_x['3'],self.coords_y['g']],
                          4:[self.coords_x['4'],self.coords_y['g']],
                          5:[self.coords_x['5'],self.coords_y['g']],
                          6:[self.coords_x['6'],self.coords_y['g']],
                          7:[self.coords_x['7'],self.coords_y['g']],
                          8:[self.coords_x['8'],self.coords_y['g']],
                          9:[self.coords_x['9'],self.coords_y['g']]}
        self.lista[SPN] = {}
        self.cnt[PN] = 10
        self.r[PN] = 0
        self.lista[PB] = {1:[self.coords_x['1'],self.coords_y['c']],
                          2:[self.coords_x['2'],self.coords_y['c']],
                          3:[self.coords_x['3'],self.coords_y['c']],
                          4:[self.coords_x['4'],self.coords_y['c']],
                          5:[self.coords_x['5'],self.coords_y['c']],
                          6:[self.coords_x['6'],self.coords_y['c']],
                          7:[self.coords_x['7'],self.coords_y['c']],
                          8:[self.coords_x['8'],self.coords_y['c']],
                          9:[self.coords_x['9'],self.coords_y['c']]}
        self.lista[SPB] = {}
        self.cnt[PB] = 10
        self.r[PB] = 0
        self.lista[LN] = {1:[self.coords_x['1'],self.coords_y['i']],
                          2:[self.coords_x['9'],self.coords_y['i']]}
        self.lista[SLN] = {}
        self.cnt[LN] = 3
        self.r[LN] = 0
        self.lista[LB] = {1:[self.coords_x['1'],self.coords_y['a']],
                          2:[self.coords_x['9'],self.coords_y['a']]}
        self.lista[SLB] = {}
        self.cnt[LB] = 3
        self.r[LB] = 0
        self.lista[NN] = {1:[self.coords_x['2'],self.coords_y['i']],
                          2:[self.coords_x['8'],self.coords_y['i']]}
        self.lista[SNN] = {}
        self.cnt[NN] = 3
        self.r[NN] = 0
        self.lista[NB] = {1:[self.coords_x['2'],self.coords_y['a']],
                          2:[self.coords_x['8'],self.coords_y['a']]}
        self.lista[SNB] = {}
        self.cnt[NB] = 3
        self.r[NB] = 0
        self.lista[SN] = {1:[self.coords_x['3'],self.coords_y['i']],
                          2:[self.coords_x['7'],self.coords_y['i']]}
        self.lista[SSN] = {}
        self.cnt[SN] = 3
        self.r[SN] = 0
        self.lista[SB] = {1:[self.coords_x['3'],self.coords_y['a']],
                          2:[self.coords_x['7'],self.coords_y['a']]}
        self.lista[SSB] = {}
        self.cnt[SB] = 3
        self.r[SB] = 0
        self.lista[GN] = {1:[self.coords_x['4'],self.coords_y['i']],
                          2:[self.coords_x['6'],self.coords_y['i']]}
        self.cnt[GN] = 3
        self.r[GN] = 0
        self.lista[GB] = {1:[self.coords_x['4'],self.coords_y['a']],
                          2:[self.coords_x['6'],self.coords_y['a']]}
        self.cnt[GB] = 3
        self.r[GB] = 0
        self.lista[TN] = {1:[self.coords_x['2'],self.coords_y['h']]}
        self.lista[STN] = {}
        self.cnt[TN] = 2
        self.r[TN] = 0
        self.lista[TB] = {1:[self.coords_x['8'],self.coords_y['b']]}
        self.lista[STB] = {}
        self.cnt[TB] = 2
        self.r[TB] = 0
        self.lista[BN] = {1:[self.coords_x['8'],self.coords_y['h']]}
        self.lista[SBN] = {}
        self.cnt[BN] = 2
        self.r[BN] = 0
        self.lista[BB] = {1:[self.coords_x['2'],self.coords_y['b']]}
        self.lista[SBB] = {}
        self.cnt[BB] = 2
        self.r[BB] = 0
        self.lista[KN] = {1:[self.coords_x['5'],self.coords_y['i']]}
        self.lista[KB] = {1:[self.coords_x['5'],self.coords_y['a']]}

    def update(self):
        if self.reverted == 1:
            self.coords_x = self.coords_ax
            self.coords_y = self.coords_ay
        else:
            self.coords_x = self.coords_bx
            self.coords_y = self.coords_by
            
    def revert(self):
        self.reverted *= -1

        revert_x = {
            269: 837,
            340: 766,
            411: 695,
            482: 624,
            553: 553,
            624: 482,
            695: 411,
            766: 340,
            837: 269
        }
        revert_y = {
            21: 589,
            92: 518,
            163: 447,
            234: 376,
            305: 305,
            376: 234,
            447: 163,
            518: 92,
            589: 21
        }
        for i in self.lista:
            for k, e in i.items():
                i[k] = [revert_x[e[0]],revert_y[e[1]]]

        #self.lista[KN] = {1:[revert_x[self.rey_n[0]],revert_y[self.rey_n[1]]]}
        #self.lista[KB] = {1:[revert_x[self.rey_b[0]],revert_y[self.rey_b[1]]]}
        
        self.update()



class sprites_manager:
    def __init__(self):
        self.probes = []
        self.imgs = []
        self.probes.append('P')
        self.probes.append('SP')
        self.probes.append('L')
        self.probes.append('SL')
        self.probes.append('N')
        self.probes.append('SN')
        self.probes.append('S')
        self.probes.append('SS')
        self.probes.append('G')
        self.probes.append('T')
        self.probes.append('ST')
        self.probes.append('B')
        self.probes.append('SB')
        self.probes.append('KN')
        self.probes.append('KB')
        for n in xrange(0, 28):
            self.imgs.append(None)

        self.probes[0] = pygame.image.load(MAINPATH + "ShogiSprites/Peon.png")
        self.probes[1] = pygame.image.load(MAINPATH + "ShogiSprites/SPeon.png")
        self.probes[2] = pygame.image.load(MAINPATH + "ShogiSprites/Lanza.png")
        self.probes[3] = pygame.image.load(MAINPATH +
                                           "ShogiSprites/SLanza.png")
        self.probes[4] = pygame.image.load(MAINPATH +
                                           "ShogiSprites/Caballo.png")
        self.probes[5] = pygame.image.load(MAINPATH +
                                           "ShogiSprites/SCaballo.png")
        self.probes[6] = pygame.image.load(MAINPATH + "ShogiSprites/Plata.png")
        self.probes[7] = pygame.image.load(MAINPATH +
                                           "ShogiSprites/SPlata.png")
        self.probes[8] = pygame.image.load(MAINPATH + "ShogiSprites/Torre.png")
        self.probes[9] = pygame.image.load(MAINPATH +
                                           "ShogiSprites/STorre.png")
        self.probes[10] = pygame.image.load(MAINPATH +
                                            "ShogiSprites/Alfil.png")
        self.probes[11] = pygame.image.load(MAINPATH +
                                            "ShogiSprites/SAlfil.png")
        self.probes[12] = pygame.image.load(MAINPATH + "ShogiSprites/Oro.png")
        self.probes[13] = pygame.image.load(MAINPATH + "ShogiSprites/ReyN.png")
        self.probes[14] = pygame.image.load(MAINPATH + "ShogiSprites/ReyB.png")

        self.revert(1)



    def revert(self, state):
        if state == 1:
            for i in xrange(0, 26):     
                if i % 2 == 0:
                    self.imgs[i] =  pygame.transform.scale(self.probes[i/2],
                                                           (70,70))
                else:
                    self.imgs[i] =  pygame.transform.rotozoom(self.imgs[i-1],
                                                              180, 1)

            self.imgs[KN] = pygame.transform.scale(self.probes[13], (70,70))
            self.imgs[KB] = pygame.transform.scale(self.probes[14], (70,70))
            self.imgs[KB] = pygame.transform.rotozoom(self.imgs[KB], 180, 1)
        else:
            for i in xrange(0, 13):     
                self.imgs[(i*2)+1] =  pygame.transform.scale(self.probes[i],
                                                                    (70,70))
                self.imgs[(i*2)] =  pygame.transform.rotozoom(
                                                 self.imgs[(i*2)+1], 180, 1)

            self.imgs[KB] = pygame.transform.scale(self.probes[14], (70,70))
            self.imgs[KN] = pygame.transform.scale(self.probes[13], (70,70))
            self.imgs[KN] = pygame.transform.rotozoom(self.imgs[KN], 180, 1)



class matrix_manager:
    def __init__(self):
        self.ADAPTX = {'9':0,'8':1,'7':2,'6':3,'5':4,'4':5,'3':6,'2':7,'1':8}
        self.ADAPTY = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8}
        self.coords_hx = {
            837:'1',
            766:'2',
            695:'3',
            624:'4',
            553:'5',
            482:'6',
            411:'7',
            340:'8',
            269:'9'
        }
        self.coords_hy = {
            589:'i',
            518:'h',
            447:'g',
            376:'f',
            305:'e',
            234:'d',
            163:'c',
            92:'b',
            21:'a'
        }
        # X es el 1er índice
        self.matrix = [
                [1,1,1,1,1,1,1,1,1],
                [0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,1,1,1],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0],
                [1,1,1,1,1,1,1,1,1],
                [0,1,0,0,0,0,0,1,0],
                [1,1,1,1,1,1,1,1,1]
        ]
    def empty(self, coords_h):
        self.matrix[self.ADAPTY[coords_h[1]]][self.ADAPTX[coords_h[0]]] = False

    def fill(self, coords_h):
        self.matrix[self.ADAPTY[coords_h[1]]][self.ADAPTX[coords_h[0]]] = True

    def get_hcoords(self, coords):
        return str(self.coords_hx[coords[0]])+str(self.coords_hy[coords[1]])


    def check_ln(self, h_begin, h_destiny):
        cursorx = self.ADAPTX[h_begin[0]]
        cursory = self.ADAPTY[h_begin[1]]
        while cursory != self.ADAPTY[h_destiny[1]]+1:
            cursory -= 1
            if self.matrix[cursory][cursorx] == True:
                return False
        return True


    def check_lb(self, h_begin, h_destiny):
        cursorx = self.ADAPTX[h_begin[0]]
        cursory = self.ADAPTY[h_begin[1]]
        while cursory != self.ADAPTY[h_destiny[1]]-1:
            cursory += 1
            if self.matrix[cursory][cursorx] == True:
                return False
        return True


    def check_t(self, h_begin, h_destiny):
        cursorx = self.ADAPTX[h_begin[0]]
        cursory = self.ADAPTY[h_begin[1]]
        destx = self.ADAPTX[h_destiny[0]]
        desty = self.ADAPTY[h_destiny[1]]

        if cursorx == destx:
            mod = 1 if cursory < desty else -1
            while cursory != desty - mod:
                cursory += mod
                if self.matrix[cursory][cursorx] == True:
                    return False
            return True
        else:
            mod = 1 if cursorx < destx else -1
            while cursorx != destx - mod:
                cursorx += mod
                if self.matrix[cursory][cursorx] == True:
                    return False
            return True


    def check_b(self, h_begin, h_destiny):
        cursorx = self.ADAPTX[h_begin[0]]
        cursory = self.ADAPTY[h_begin[1]]
        destx = self.ADAPTX[h_destiny[0]]
        desty = self.ADAPTY[h_destiny[1]]

        modx = 1 if cursorx < destx else -1
        mody = 1 if cursory < desty else -1

        while (cursorx != destx - modx) or (cursory != desty - mody):
            cursorx += modx
            cursory += mody
            if self.matrix[cursory][cursorx] == True:
                return False
        return True



class input_manager:
    def __init__(self, input_text):
        self.raw = input_text.replace('\n','')
        self.movs = None
        self.metadata = None
        self.comments = []
        self.sente = None
        self.gote = None
        self.get_metadata()
        self.get_names()
        self.prepare_movs()


    def get_metadata(self):
        reg = re.compile(r'\[[^\[\]]*\]')
        self.metadata = reg.findall(self.raw)
        for e in self.metadata:
            self.raw = self.raw.replace(e, '')


    def get_names(self):
        sente = re.compile(
            r'\[([Ss]ente|[Bb]lack)[:\s][^\[\]]*"([a-zA-z0-9][^\[\]]*)"\s*\]')
        gote = re.compile(
            r'\[([Gg]ote|[Ww]hite)[:\s][^\[\]]*"([a-zA-z0-9][^\[\]]*)"\s*\]')

        for e in self.metadata:
            if sente.match(e):
                self.sente = sente.match(e).group(2)
            elif gote.match(e):
                self.gote = gote.match(e).group(2)

    
    def prepare_movs(self):
        reg = re.compile(
              r'(\+?[P|L|N|S|G|K|R|B](\d[a-i])?[-|x|*]\d[a-i][=|\+]?)')
        moves = reg.findall(self.raw)
        output = ''
        if moves == []:
            tkMessageBox.showerror("NO NOTATIONS FOUND",
                "This file doesn't contain correct shogi western notations.")
            exit()
        for i in xrange(0, len(moves)):
            if output != '':
                output += '\n'
            if str(type(moves[i])) == "<type 'tuple'>":    
                output += str(i+1) + ' - ' +moves[i][0]
            else:
                output += str(i+1) + ' - ' +moves[i]
        self.movs = output
