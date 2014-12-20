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
		D -> Forward
		A -> Backwards
		R -> Reverse board

	Open the files in "games_recorded" directory to see how it works.
"""

import pygame, sys, re
from pygame.locals import *
from managers import *

pygame.init()
#reloj = pygame.time.Clock()
size = width, height = 1200,760

SCREEN = pygame.display.set_mode(size)
FONT = pygame.font.SysFont("monospace", 14)
pygame.display.set_caption("ShogiReader - Reproductor de partidas grabadas")

# *** POSITIONS TABLE and Pieces arrays ***
lamesa = coords_manager()
matrix = matrix_manager()

# *** Motion log array ***
history = []

# *** Load input file ***

import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()
if file_path == '':
	exit()
partida = open(file_path, 'r')

rawgame = partida.read()
game_data = input_manager(rawgame)
movs = game_data.movs.splitlines()

partida.close()

# ******* TABLERO ********

r = 235
g = 220
b = 180

bg = int(r), int(g), int(b)

def redraw():
#	global FONT
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

# *** ALGORYTHM TO READ NOTATION AND TRANSFORM IT INTO DATA EXECUTABLE FORWARD AND BACKWARDS ***

reg = re.compile('^\s*(\d+)\s*-\s*(\+?[P|L|N|S|G|K|R|B](\d[a-i])?)([-|x|*])(\d[a-i][=|\+]?)$')
for e in movs:
	kind = ''
	action = None
	promoting = False
	piece_respawn = ''
	piece_x = 0
	piece_y = 0
	frag = reg.match(e)
	destiny = [lamesa.coords_x[frag.group(5)[0]],lamesa.coords_y[frag.group(5)[1]]]
	destiny_h = frag.group(5)
	if len(frag.group(5)) > 2:
		if frag.group(5)[2] == '+':
			promoting = True
	if (len(frag.group(2)) > 1 and frag.group(2)[0] != '+') or (len(frag.group(2)) > 2 and frag.group(2)[0] == '+'):
		if frag.group(2)[0] == '+':
			kind = frag.group(2)[0:2]
			piece_x = lamesa.coords_x[frag.group(2)[2]]
			piece_y = lamesa.coords_y[frag.group(2)[3]]
		else:
			kind = frag.group(2)[0]
			piece_x = lamesa.coords_x[frag.group(2)[1]]
			piece_y = lamesa.coords_y[frag.group(2)[2]]
	else:
		kind = frag.group(2)
	if frag.group(4) == 'x':
		action = 1
	elif frag.group(4) == '*':
		action = 2
	elif frag.group(4) == '-':
		action = 0

	if action == 1:
		if int(frag.group(1)) % 2 == 1: #Negras
			found = False
			while found == False:
				for k, e in lamesa.lista_pb.items():
					if e == destiny:
						del lamesa.lista_pb[k]
						lamesa.rpn += 1
						piece_respawn = 'lista_pb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_spb.items():
					if e == destiny:
						del lamesa.lista_spb[k]
						lamesa.rpn += 1
						piece_respawn = 'lista_spb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_lb.items():
					if e == destiny:
						del lamesa.lista_lb[k]
						lamesa.rln += 1
						piece_respawn = 'lista_lb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_slb.items():
					if e == destiny:
						del lamesa.lista_slb[k]
						lamesa.rln += 1
						piece_respawn = 'lista_slb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_nb.items():
					if e == destiny:
						del lamesa.lista_nb[k]
						lamesa.rnn += 1
						piece_respawn = 'lista_nb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_snb.items():
					if e == destiny:
						del lamesa.lista_snb[k]
						lamesa.rnn += 1
						piece_respawn = 'lista_snb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_sb.items():
					if e == destiny:
						del lamesa.lista_sb[k]
						lamesa.rsn += 1
						piece_respawn = 'lista_sb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_ssb.items():
					if e == destiny:
						del lamesa.lista_ssb[k]
						lamesa.rsn += 1
						piece_respawn = 'lista_ssb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_gb.items():
					if e == destiny:
						del lamesa.lista_gb[k]
						lamesa.rgn += 1
						piece_respawn = 'lista_gb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_tb.items():
					if e == destiny:
						del lamesa.lista_tb[k]
						lamesa.rtn += 1
						piece_respawn = 'lista_tb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_stb.items():
					if e == destiny:
						del lamesa.lista_stb[k]
						lamesa.rtn += 1
						piece_respawn = 'lista_stb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_bb.items():
					if e == destiny:
						del lamesa.lista_bb[k]
						lamesa.rbn += 1
						piece_respawn = 'lista_bb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_sbb.items():
					if e == destiny:
						del lamesa.lista_sbb[k]
						lamesa.rbn += 1
						piece_respawn = 'lista_sbb['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
		else: # Blancas
			found = False
			while found == False:
				for k, e in lamesa.lista_pn.items():
					if e == destiny:
						del lamesa.lista_pn[k]
						lamesa.rpb += 1
						piece_respawn = 'lista_pn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_spn.items():
					if e == destiny:
						del lamesa.lista_spn[k]
						lamesa.rpb += 1
						piece_respawn = 'lista_spn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_ln.items():
					if e == destiny:
						del lamesa.lista_ln[k]
						lamesa.rlb += 1
						piece_respawn = 'lista_ln['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_sln.items():
					if e == destiny:
						del lamesa.lista_sln[k]
						lamesa.rlb += 1
						piece_respawn = 'lista_sln['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_nn.items():
					if e == destiny:
						del lamesa.lista_nn[k]
						lamesa.rnb += 1
						piece_respawn = 'lista_nn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_snn.items():
					if e == destiny:
						del lamesa.lista_snn[k]
						lamesa.rnb += 1
						piece_respawn = 'lista_snn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_sn.items():
					if e == destiny:
						del lamesa.lista_sn[k]
						lamesa.rsb += 1
						piece_respawn = 'lista_sn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_ssn.items():
					if e == destiny:
						del lamesa.lista_ssn[k]
						lamesa.rsb += 1
						piece_respawn = 'lista_ssn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_gn.items():
					if e == destiny:
						del lamesa.lista_gn[k]
						lamesa.rgb += 1
						piece_respawn = 'lista_gn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_tn.items():
					if e == destiny:
						del lamesa.lista_tn[k]
						lamesa.rtb += 1
						piece_respawn = 'lista_tn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_stn.items():
					if e == destiny:
						del lamesa.lista_stn[k]
						lamesa.rtb += 1
						piece_respawn = 'lista_stn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_bn.items():
					if e == destiny:
						del lamesa.lista_bn[k]
						lamesa.rbb += 1
						piece_respawn = 'lista_bn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break
				if found == True:
					 break
				for k, e in lamesa.lista_sbn.items():
					if e == destiny:
						del lamesa.lista_sbn[k]
						lamesa.rbb += 1
						piece_respawn = 'lista_sbn['+(str)(k)+']=[lamesa.coords_x["'+destiny_h[0]+'"],lamesa.coords_y["'+destiny_h[1]+'"]]'
						found = True
						break


	if piece_x == 0 and action != 2:
		if int(frag.group(1)) % 2 == 1: #Negras
			if kind == 'P':
				for k, pn in lamesa.lista_pn.items():
					if destiny[0] == pn[0] and destiny[1] == pn[1]-71:
						history.append(['lista_pn['+(str)(k)+']',[0,-71], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_pn[k]))
						lamesa.lista_pn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_pn[k]
							lamesa.lista_spn[k] = destiny
						break
			if kind == 'L':
				for k, ln in lamesa.lista_ln.items():
					if destiny[0] == ln[0] and destiny[1] < ln[1]:
						if matrix.check_ln(matrix.get_hcoords(ln),destiny_h) == True:
							history.append(['lista_ln['+(str)(k)+']',[0,destiny[1]-ln[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_ln[k]))
							lamesa.lista_ln[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_ln[k]
								lamesa.lista_sln[k] = destiny
							break
			if kind == 'N':
				for k, nn in lamesa.lista_nn.items():
					if (destiny[0] == nn[0]+71 or destiny[0] == nn[0]-71 ) and destiny[1] == nn[1]-142:
						history.append(['lista_nn['+(str)(k)+']',[destiny[0]-nn[0],destiny[1]-nn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_nn[k]))
						lamesa.lista_nn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_nn[k]
							lamesa.lista_snn[k] = destiny
						break
			if kind == 'S':
				for k, sn in lamesa.lista_sn.items():
					if (destiny[0] <= sn[0]+71 and destiny[0] >= sn[0]-71 and destiny[1] == sn[1]-71) or ((destiny[0] == sn[0]+71 or destiny[0] == sn[0]-71) and destiny[1] == sn[1]+71):
						history.append(['lista_sn['+(str)(k)+']',[destiny[0]-sn[0],destiny[1]-sn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_sn[k]))
						lamesa.lista_sn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_sn[k]
							lamesa.lista_ssn[k] = destiny
						break
			if kind == 'G':
				for k, gn in lamesa.lista_gn.items():
					if (destiny[0] <= gn[0]+71 and destiny[0] >= gn[0]-71 and destiny[1] == gn[1]-71) or ((destiny[0] == gn[0]+71 or destiny[0] == gn[0]-71) and destiny[1] == gn[1]) or (destiny[0] == gn[0] and destiny[1] == gn[1]+71):
						history.append(['lista_gn['+(str)(k)+']',[destiny[0]-gn[0],destiny[1]-gn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_gn[k]))
						lamesa.lista_gn[k] = destiny
						matrix.fill(destiny_h)
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lamesa.lista_s'+mem+'n.items():\n\t'
				statem+= 'if (destiny[0] <= j[0]+71 and destiny[0] >= j[0]-71 and destiny[1] == j[1]-71) or ((destiny[0] == j[0]+71 or destiny[0] == j[0]-71) and destiny[1] == j[1]) or (destiny[0] == j[0] and destiny[1] == j[1]+71):\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'n["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',\''+piece_respawn+'\'])\n\t\t'
				statem+= 'matrix.empty(matrix.get_hcoords(lamesa.lista_s'+mem+'n[k]))\n\t\t'
				statem+= 'lamesa.lista_s'+mem+'n[k] = destiny\n\t\t'
				statem+= 'matrix.fill(destiny_h)\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tn in lamesa.lista_tn.items():
					if (destiny[0] == tn[0]) != (destiny[1] == tn[1]):
						if matrix.check_t(matrix.get_hcoords(tn),destiny_h) == True:
							history.append(['lista_tn['+(str)(k)+']',[destiny[0]-tn[0],destiny[1]-tn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_tn[k]))
							lamesa.lista_tn[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_tn[k]
								lamesa.lista_stn[k] = destiny
							break
			if kind == '+R':
				for k, stn in lamesa.lista_stn.items():
					if ((destiny[0] == stn[0]) != (destiny[1] == stn[1])) or (destiny[0] <= stn[0]+71 and destiny[0] >= stn[0]-71 and destiny[1] <= stn[1]+71 and destiny[1] >= stn[1]-71):
						if ((destiny[0] == stn[0]) != (destiny[1] == stn[1]) and matrix.check_t(matrix.get_hcoords(stn),destiny_h) == True) or not((destiny[0] == stn[0]) != (destiny[1] == stn[1])):
							history.append(['lista_stn['+(str)(k)+']',[destiny[0]-stn[0],destiny[1]-stn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_stn[k]))
							lamesa.lista_stn[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'B':
				for k, bn in lamesa.lista_bn.items():
					if abs(destiny[0]-bn[0]) == abs(destiny[1]-bn[1]):
						if matrix.check_b(matrix.get_hcoords(bn),destiny_h) == True:
							history.append(['lista_bn['+(str)(k)+']',[destiny[0]-bn[0],destiny[1]-bn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_bn[k]))
							lamesa.lista_bn[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_bn[k]
								lamesa.lista_sbn[k] = destiny
							break
			if kind == '+B':
				for k, sbn in lamesa.lista_sbn.items():
					if (abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) or (destiny[0] <= sbn[0]+71 and destiny[0] >= sbn[0]-71 and destiny[1] <= sbn[1]+71 and destiny[1] >= sbn[1]-71):
						if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) and matrix.check_b(matrix.get_hcoords(sbn),destiny_h) == True) or not(abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])):
							history.append(['lista_sbn['+(str)(k)+']',[destiny[0]-sbn[0],destiny[1]-sbn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_sbn[k]))
							lamesa.lista_sbn[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'K':
				if destiny[0] <= lamesa.rey_n[0]+71 and destiny[0] >= lamesa.rey_n[0]-71 and destiny[1] <= lamesa.rey_n[1]+71 and destiny[1] >= lamesa.rey_n[1]-71:
					history.append(['rey_n',[destiny[0]-lamesa.rey_n[0],destiny[1]-lamesa.rey_n[1]], action, promoting, piece_respawn])
					matrix.empty(matrix.get_hcoords(lamesa.rey_n))
					lamesa.rey_n = destiny
					matrix.fill(destiny_h)
		else: #Blancas
			if kind == 'P':
				for k, pb in lamesa.lista_pb.items():
					if destiny[0] == pb[0] and destiny[1] == pb[1]+71:
						history.append(['lista_pb['+(str)(k)+']',[0, 71], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_pb[k]))
						lamesa.lista_pb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_pb[k]
							lamesa.lista_spb[k] = destiny
						break
			if kind == 'L':
				for k, lb in lamesa.lista_lb.items():
					if destiny[0] == lb[0] and destiny[1] > lb[1]:
						if matrix.check_lb(matrix.get_hcoords(lb),destiny_h) == True:
							history.append(['lista_lb['+(str)(k)+']',[0,destiny[1]-lb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_lb[k]))
							lamesa.lista_lb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_lb[k]
								lamesa.lista_slb[k] = destiny
							break
			if kind == 'N':
				for k, nb in lamesa.lista_nb.items():
					if (destiny[0] == nb[0]+71 or destiny[0] == nb[0]-71 ) and destiny[1] == nb[1]+142:
						history.append(['lista_nb['+(str)(k)+']',[destiny[0]-nb[0],destiny[1]-nb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_nb[k]))
						lamesa.lista_nb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_nb[k]
							lamesa.lista_snb[k] = destiny
						break
			if kind == 'S':
				for k, sb in lamesa.lista_sb.items():
					if (destiny[0] <= sb[0]+71 and destiny[0] >= sb[0]-71 and destiny[1] == sb[1]+71) or ((destiny[0] == sb[0]+71 or destiny[0] == sb[0]-71) and destiny[1] == sb[1]-71):
						history.append(['lista_sb['+(str)(k)+']',[destiny[0]-sb[0],destiny[1]-sb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_sb[k]))
						lamesa.lista_sb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_sb[k]
							lamesa.lista_ssb[k] = destiny
						break
			if kind == 'G':
				for k, gb in lamesa.lista_gb.items():
					if (destiny[0] <= gb[0]+71 and destiny[0] >= gb[0]-71 and destiny[1] == gb[1]+71) or ((destiny[0] == gb[0]+71 or destiny[0] == gb[0]-71) and destiny[1] == gb[1]) or (destiny[0] == gb[0] and destiny[1] == gb[1]-71):
						history.append(['lista_gb['+(str)(k)+']',[destiny[0]-gb[0],destiny[1]-gb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_gb[k]))
						lamesa.lista_gb[k] = destiny
						matrix.fill(destiny_h)
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lamesa.lista_s'+mem+'b.items():\n\t'
				statem+= 'if (destiny[0] <= j[0]+71 and destiny[0] >= j[0]-71 and destiny[1] == j[1]+71) or ((destiny[0] == j[0]+71 or destiny[0] == j[0]-71) and destiny[1] == j[1]) or (destiny[0] == j[0] and destiny[1] == j[1]-71):\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'b["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',\''+piece_respawn+'\'])\n\t\t'
				statem+= 'matrix.empty(matrix.get_hcoords(lamesa.lista_s'+mem+'b[k]))\n\t\t'
				statem+= 'lamesa.lista_s'+mem+'b[k] = destiny\n\t\t'
				statem+= 'matrix.fill(destiny_h)\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tb in lamesa.lista_tb.items():
					if (destiny[0] == tb[0]) != (destiny[1] == tb[1]):
						if matrix.check_t(matrix.get_hcoords(tb),destiny_h) == True:
							history.append(['lista_tb['+(str)(k)+']',[destiny[0]-tb[0],destiny[1]-tb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_tb[k]))
							lamesa.lista_tb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_tb[k]
								lamesa.lista_stb[k] = destiny
							break
			if kind == '+R':
				for k, stb in lamesa.lista_stb.items():
					if ((destiny[0] == stb[0]) != (destiny[1] == stb[1])) or (destiny[0] <= stb[0]+71 and destiny[0] >= stb[0]-71 and destiny[1] <= stb[1]+71 and destiny[1] >= stb[1]-71):
						if ((destiny[0] == stb[0]) != (destiny[1] == stb[1]) and matrix.check_t(matrix.get_hcoords(stb),destiny_h) == True) or not((destiny[0] == stb[0]) != (destiny[1] == stb[1])):
							history.append(['lista_stb['+(str)(k)+']',[destiny[0]-stb[0],destiny[1]-stb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_stb[k]))
							lamesa.lista_stb[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'B':
				for k, bb in lamesa.lista_bb.items():
					if abs(destiny[0]-bb[0]) == abs(destiny[1]-bb[1]):
						if matrix.check_b(matrix.get_hcoords(bb),destiny_h) == True:
							history.append(['lista_bb['+(str)(k)+']',[destiny[0]-bb[0],destiny[1]-bb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_bb[k]))
							lamesa.lista_bb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_bb[k]
								lamesa.lista_sbb[k] = destiny
							break
			if kind == '+B':
				for k, sbb in lamesa.lista_sbb.items():
					if (abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) or (destiny[0] <= sbb[0]+71 and destiny[0] >= sbb[0]-71 and destiny[1] <= sbb[1]+71 and destiny[1] >= sbb[1]-71):
						if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) and matrix.check_b(matrix.get_hcoords(sbb),destiny_h) == True) or not(abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])):
							history.append(['lista_sbb['+(str)(k)+']',[destiny[0]-sbb[0],destiny[1]-sbb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_sbb[k]))
							lamesa.lista_sbb[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'K':
				if destiny[0] <= lamesa.rey_b[0]+71 and destiny[0] >= lamesa.rey_b[0]-71 and destiny[1] <= lamesa.rey_b[1]+71 and destiny[1] >= lamesa.rey_b[1]-71:
					history.append(['rey_b',[destiny[0]-lamesa.rey_b[0],destiny[1]-lamesa.rey_b[1]], action, promoting, piece_respawn])
					matrix.empty(matrix.get_hcoords(lamesa.rey_b))
					lamesa.rey_b = destiny
					matrix.fill(destiny_h)
	elif action != 2:
		if int(frag.group(1)) % 2 == 1: #Negras
			if kind == 'P':
				for k, pn in lamesa.lista_pn.items():
					if pn[0] == piece_x and pn[1] == piece_y:
						history.append(['lista_pn['+(str)(k)+']',[0,-71], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_pn[k]))
						lamesa.lista_pn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_pn[k]
							lamesa.lista_spn[k] = destiny
						break
			if kind == 'L':
				for k, ln in lamesa.lista_ln.items():
					if ln[0] == piece_x and ln[1] == piece_y:
						if matrix.check_ln(matrix.get_hcoords(ln),destiny_h) == True:
							history.append(['lista_ln['+(str)(k)+']',[0,destiny[1]-ln[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_ln[k]))
							lamesa.lista_ln[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_ln[k]
								lamesa.lista_sln[k] = destiny
							break
			if kind == 'N':
				for k, nn in lamesa.lista_nn.items():
					if nn[0] == piece_x and nn[1] == piece_y:
						history.append(['lista_nn['+(str)(k)+']',[destiny[0]-nn[0],destiny[1]-nn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_nn[k]))
						lamesa.lista_nn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_nn[k]
							lamesa.lista_snn[k] = destiny
						break
			if kind == 'S':
				for k, sn in lamesa.lista_sn.items():
					if sn[0] == piece_x and sn[1] == piece_y:
						history.append(['lista_sn['+(str)(k)+']',[destiny[0]-sn[0],destiny[1]-sn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_sn[k]))
						lamesa.lista_sn[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_sn[k]
							lamesa.lista_ssn[k] = destiny
						break
			if kind == 'G':
				for k, gn in lamesa.lista_gn.items():
					if gn[0] == piece_x and gn[1] == piece_y:
						history.append(['lista_gn['+(str)(k)+']',[destiny[0]-gn[0],destiny[1]-gn[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_gn[k]))
						lamesa.lista_gn[k] = destiny
						matrix.fill(destiny_h)
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lamesa.lista_s'+mem+'n.items():\n\t'
				statem+= 'if j[0] == piece_x and j[1] == piece_y:\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'n["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',\''+piece_respawn+'\'])\n\t\t'
				statem+= 'matrix.empty(matrix.get_hcoords(lamesa.lista_s'+mem+'n[k]))\n\t\t'
				statem+= 'lamesa.lista_s'+mem+'n[k] = destiny\n\t\t'
				statem+= 'matrix.fill(destiny_h)\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tn in lamesa.lista_tn.items():
					if tn[0] == piece_x and tn[1] == piece_y:
						if matrix.check_t(matrix.get_hcoords(tn),destiny_h) == True:
							history.append(['lista_tn['+(str)(k)+']',[destiny[0]-tn[0],destiny[1]-tn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_tn[k]))
							lamesa.lista_tn[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_tn[k]
								lamesa.lista_stn[k] = destiny
							break
			if kind == '+R':
				for k, stn in lamesa.lista_stn.items():
					if stn[0] == piece_x and stn[1] == piece_y:
						if ((destiny[0] == stn[0]) != (destiny[1] == stn[1]) and matrix.check_t(matrix.get_hcoords(stn),destiny_h) == True) or not((destiny[0] == stn[0]) != (destiny[1] == stn[1])):
							history.append(['lista_stn['+(str)(k)+']',[destiny[0]-stn[0],destiny[1]-stn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_stn[k]))
							lamesa.lista_stn[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'B':
				for k, bn in lamesa.lista_bn.items():
					if bn[0] == piece_x and bn[1] == piece_y:
						if matrix.check_b(matrix.get_hcoords(bn),destiny_h) == True:
							history.append(['lista_bn['+(str)(k)+']',[destiny[0]-bn[0],destiny[1]-bn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_bn[k]))
							lamesa.lista_bn[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_bn[k]
								lamesa.lista_sbn[k] = destiny
							break
			if kind == '+B':
				for k, sbn in lamesa.lista_sbn.items():
					if sbn[0] == piece_x and sbn[1] == piece_y:
						if ((abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) and matrix.check_b(matrix.get_hcoords(sbn),destiny_h) == True) or not(abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])):
							history.append(['lista_sbn['+(str)(k)+']',[destiny[0]-sbn[0],destiny[1]-sbn[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_sbn[k]))
							lamesa.lista_sbn[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'K':
				if lamesa.rey_n[0] == piece_x and lamesa.rey_n[1] == piece_y:
					history.append(['rey_n',[destiny[0]-lamesa.rey_n[0],destiny[1]-lamesa.rey_n[1]], action, promoting, piece_respawn])
					matrix.empty(matrix.get_hcoords(lamesa.rey_n))
					lamesa.rey_n = destiny
					matrix.fill(destiny_h)
		else: # Blancas
			if kind == 'P':
				for k, pb in lamesa.lista_pb.items():
					if pb[0] == piece_x and pb[1] == piece_y:
						history.append(['lista_pb['+(str)(k)+']',[0,+71], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_pb[k]))
						lamesa.lista_pb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_pb[k]
							lamesa.lista_spb[k] = destiny
						break
			if kind == 'L':
				for k, lb in lamesa.lista_lb.items():
					if lb[0] == piece_x and lb[1] == piece_y:
						if matrix.check_lb(matrix.get_hcoords(lb),destiny_h) == True:
							history.append(['lista_lb['+(str)(k)+']',[0,destiny[1]-lb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_lb[k]))
							lamesa.lista_lb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_lb[k]
								lamesa.lista_slb[k] = destiny
							break
			if kind == 'N':
				for k, nb in lamesa.lista_nb.items():
					if nb[0] == piece_x and nb[1] == piece_y:
						history.append(['lista_nb['+(str)(k)+']',[destiny[0]-nb[0],destiny[1]-nb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_nb[k]))
						lamesa.lista_nb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_nb[k]
							lamesa.lista_snb[k] = destiny
						break
			if kind == 'S':
				for k, sb in lamesa.lista_sb.items():
					if sb[0] == piece_x and sb[1] == piece_y:
						history.append(['lista_sb['+(str)(k)+']',[destiny[0]-sb[0],destiny[1]-sb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_sb[k]))
						lamesa.lista_sb[k] = destiny
						matrix.fill(destiny_h)
						if promoting == True:
							del lamesa.lista_sb[k]
							lamesa.lista_ssb[k] = destiny
						break
			if kind == 'G':
				for k, gb in lamesa.lista_gb.items():
					if gb[0] == piece_x and gb[1] == piece_y:
						history.append(['lista_gb['+(str)(k)+']',[destiny[0]-gb[0],destiny[1]-gb[1]], action, promoting, piece_respawn])
						matrix.empty(matrix.get_hcoords(lamesa.lista_gb[k]))
						lamesa.lista_gb[k] = destiny
						matrix.fill(destiny_h)
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lamesa.lista_s'+mem+'b.items():\n\t'
				statem+= 'if j[0] == piece_x and j[1] == piece_y:\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'b["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',\''+piece_respawn+'\'])\n\t\t'
				statem+= 'matrix.empty(matrix.get_hcoords(lamesa.lista_s'+mem+'b[k]))\n\t\t'
				statem+= 'lamesa.lista_s'+mem+'b[k] = destiny\n\t\t'
				statem+= 'matrix.fill(destiny_h)\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tb in lamesa.lista_tb.items():
					if tb[0] == piece_x and tb[1] == piece_y:
						if matrix.check_t(matrix.get_hcoords(tb),destiny_h) == True:
							history.append(['lista_tb['+(str)(k)+']',[destiny[0]-tb[0],destiny[1]-tb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_tb[k]))
							lamesa.lista_tb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_tb[k]
								lamesa.lista_stb[k] = destiny
							break
			if kind == '+R':
				for k, stb in lamesa.lista_stb.items():
					if stb[0] == piece_x and stb[1] == piece_y:
						if ((destiny[0] == stb[0]) != (destiny[1] == stb[1]) and matrix.check_t(matrix.get_hcoords(stb),destiny_h) == True) or not((destiny[0] == stb[0]) != (destiny[1] == stb[1])):
							history.append(['lista_stb['+(str)(k)+']',[destiny[0]-stb[0],destiny[1]-stb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_stb[k]))
							lamesa.lista_stb[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'B':
				for k, bb in lamesa.lista_bb.items():
					if bb[0] == piece_x and bb[1] == piece_y:
						if matrix.check_b(matrix.get_hcoords(bb),destiny_h) == True:
							history.append(['lista_bb['+(str)(k)+']',[destiny[0]-bb[0],destiny[1]-bb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_bb[k]))
							lamesa.lista_bb[k] = destiny
							matrix.fill(destiny_h)
							if promoting == True:
								del lamesa.lista_bb[k]
								lamesa.lista_sbb[k] = destiny
							break
			if kind == '+B':
				for k, sbb in lamesa.lista_sbb.items():
					if sbb[0] == piece_x and sbb[1] == piece_y:
						if ((abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) and matrix.check_b(matrix.get_hcoords(sbb),destiny_h) == True) or not(abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])):
							history.append(['lista_sbb['+(str)(k)+']',[destiny[0]-sbb[0],destiny[1]-sbb[1]], action, promoting, piece_respawn])
							matrix.empty(matrix.get_hcoords(lamesa.lista_sbb[k]))
							lamesa.lista_sbb[k] = destiny
							matrix.fill(destiny_h)
							break
			if kind == 'K':
				if lamesa.rey_b[0] == piece_x and lamesa.rey_b[1] == piece_y:
					history.append(['rey_b',[destiny[0]-lamesa.rey_b[0],destiny[1]-lamesa.rey_b[1]], action, promoting, piece_respawn])
					matrix.empty(matrix.get_hcoords(lamesa.rey_b))
					lamesa.rey_b = destiny
					matrix.fill(destiny_h)
	else: # Action=2 (reingreso)
		if int(frag.group(1)) % 2 == 1: #Negras
			player = 'n'
		else:
			player = 'b'

		if kind == 'P':
			if player == 'n':
				history.append([['pn',lamesa.cnt_pn], destiny_h, action, promoting, piece_respawn])	
				lamesa.lista_pn[lamesa.cnt_pn] = destiny
				lamesa.cnt_pn += 1
				lamesa.rpn -= 1
			else:
				history.append([['pb',lamesa.cnt_pb], destiny_h, action, promoting, piece_respawn])	
				lamesa.lista_pb[lamesa.cnt_pb] = destiny
				lamesa.cnt_pb += 1
				lamesa.rpb -= 1
		if kind == 'L':
			if player == 'n':
				history.append([['ln',lamesa.cnt_ln], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_ln[lamesa.cnt_ln] = destiny
				lamesa.cnt_ln += 1
				lamesa.rln -= 1
			else:
				history.append([['lb',lamesa.cnt_lb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_lb[lamesa.cnt_lb] = destiny
				lamesa.cnt_lb += 1
				lamesa.rlb -= 1
		if kind == 'N':
			if player == 'n':
				history.append([['nn',lamesa.cnt_nn], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_nn[lamesa.cnt_nn] = destiny
				lamesa.cnt_nn += 1
				lamesa.rnn -= 1
			else:
				history.append([['nb',lamesa.cnt_nb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_nb[lamesa.cnt_nb] = destiny
				lamesa.cnt_nb += 1
				lamesa.rnb -= 1
		if kind == 'S':
			if player == 'n':
				history.append([['sn',lamesa.cnt_sn], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_sn[lamesa.cnt_sn] = destiny
				lamesa.cnt_sn += 1
				lamesa.rsn -= 1
			else:
				history.append([['sb',lamesa.cnt_sb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_sb[lamesa.cnt_sb] = destiny
				lamesa.cnt_sb += 1
				lamesa.rsb -= 1
		if kind == 'G':
			if player == 'n':
				history.append([['gn',lamesa.cnt_gn], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_gn[lamesa.cnt_gn] = destiny
				lamesa.cnt_gn += 1
				lamesa.rgn -= 1
			else:
				history.append([['gb',lamesa.cnt_gb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_gb[lamesa.cnt_gb] = destiny
				lamesa.cnt_gb += 1
				lamesa.rgb -= 1
		if kind == 'R':
			if player == 'n':
				history.append([['tn',lamesa.cnt_tn], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_tn[lamesa.cnt_tn] = destiny
				lamesa.cnt_tn += 1
				lamesa.rtn -= 1
			else:
				history.append([['tb',lamesa.cnt_tb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_tb[lamesa.cnt_tb] = destiny
				lamesa.cnt_tb += 1
				lamesa.rtb -= 1
		if kind == 'B':
			if player == 'n':
				history.append([['bn',lamesa.cnt_bn], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_bn[lamesa.cnt_bn] = destiny
				lamesa.cnt_bn += 1
				lamesa.rbn -= 1
			else:
				history.append([['bb',lamesa.cnt_bb], destiny_h, action, promoting, piece_respawn])
				lamesa.lista_bb[lamesa.cnt_bb] = destiny
				lamesa.cnt_bb += 1
				lamesa.rbb -= 1
		matrix.fill(destiny_h)

	#Loading progress
	#print len(history)

# *** sprites ***
sprites = sprites_manager()

pos = 0
max_history = len(history)

#TODO:
#   History registries should be optimized to prevent the mess in move_forward() 
# and move backwards() to handle some extraordinary situations. When I say "mess"
# I mean that some instructions are excessively complicated I guess, they are doing
# thing that I'm sure can be achieved in a more simple way.

def move_forward():
	global pos
	output = ''
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
			prueba = re.match('^.*\[(.*)\]$', history[pos][0])
			statem = 'prueba2=lamesa.'+history[pos][0]
			exec statem
			statem = 'del lamesa.'+history[pos][0]
			exec statem
			prueba4 = re.match('^.*_(.*)\[.*\]$', history[pos][0])
			statem = 'lamesa.lista_s'+prueba4.group(1)+'['+prueba.group(1)+']=['+(str)(prueba2[0])+','+(str)(prueba2[1])+']'
			exec statem
	if history[pos][4] != '':#Piece captured that has to be respawn backwards
		# TODO Avoid regexp abuse
		frag = re.match('^(lista_(.*)\[.*\])=\[.*,.*\]$', history[pos][4])
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

def previous_highlight(cursor):
	global history, SCREEN
	if history[cursor-1][2] != 2:
		if cursor > 0:
			obj = history[cursor-1][0]
			if history[cursor-1][3] == True:
				frag = re.match('^lista_(.*\[.*\])$', obj)
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
	global pos
	pos -= 1
	output = ''
	if history[pos][2] == 2:
		statem = 'del lamesa.lista_'+history[pos][0][0]+'['+(str)(history[pos][0][1])+']'
		exec statem
		output = 'lamesa.r'+history[pos][0][0]+' += 1'
	else:
		if history[pos][3] == True:
			#TODO Avoid regexp abuse
			prueba = re.match('^.*\[(.*)\]$', history[pos][0])
			prueba4 = re.match('^.*_(.*)\[.*\]$', history[pos][0])
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
		frag = re.match('^lista_(.*)\[.*\]=\[.*,.*\]$', history[pos][4])
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
	SCREEN.blit(label2, (930,360))

# *** Pieces arrays *** -> restart
lamesa.begin()
show_names()
matrix = None

cnt_fw = 0
cnt_bw = 0
hold_fw = False
hold_bw = False
delay = 10
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
#	for event in pygame.event.get():
	if event.type == pygame.QUIT:
		sys.exit()
	elif event.type == KEYDOWN and event.key == K_ESCAPE:
		sys.exit()
	elif event.type == KEYDOWN and event.key == K_d and pos < max_history:
		redraw()
		show_names()
		exec move_forward()
		hold_fw = True
		if cnt_fw < 10:
			cnt_fw += 1
	elif event.type == KEYUP and event.key == K_d:
		hold_fw = False
		cnt_fw = 0
	elif event.type == KEYDOWN and event.key == K_a and pos > 0:
		redraw()
		show_names()
		exec move_back()
		hold_bw = True
		if cnt_bw < 10:
			cnt_bw += 1
	elif event.type == KEYUP and event.key == K_a:
		hold_bw = False
		cnt_bw = 0
	elif event.type == KEYDOWN and event.key == K_r:
		lamesa.revert()
		redraw()
		show_names()
		# Invert sprites
		sprites.revert(lamesa.reverted)
		previous_highlight(pos)

#		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
#			silent.play()
#		elif event.type == KEYDOWN and event.key == K_SPACE:
#			pygame.image.save(screen, "screenshot.png")

#	mx,my = pygame.mouse.get_pos()
#	pygame.draw.line(SCREEN, (0,0,0), (20,20), (mx,my))

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
		mod = i*10
		SCREEN.blit(sprites.pn_img, (res_n['p'][0]+mod, res_n['p'][1]))	
	for i in xrange(0, lamesa.rpb):
		mod = i*10
		SCREEN.blit(sprites.pb_img, (res_b['p'][0]+mod, res_b['p'][1]))	
	for i in xrange(0, lamesa.rln):
		mod = i*10
		SCREEN.blit(sprites.ln_img, (res_n['l'][0]+mod, res_n['l'][1]))	
	for i in xrange(0, lamesa.rlb):
		mod = i*10
		SCREEN.blit(sprites.lb_img, (res_b['l'][0]+mod, res_b['l'][1]))	
	for i in xrange(0, lamesa.rnn):
		mod = i*10
		SCREEN.blit(sprites.nn_img, (res_n['n'][0]+mod, res_n['n'][1]))	
	for i in xrange(0, lamesa.rnb):
		mod = i*10
		SCREEN.blit(sprites.nb_img, (res_b['n'][0]+mod, res_b['n'][1]))	
	for i in xrange(0, lamesa.rsn):
		mod = i*10
		SCREEN.blit(sprites.sn_img, (res_n['s'][0]+mod, res_n['s'][1]))	
	for i in xrange(0, lamesa.rsb):
		mod = i*10
		SCREEN.blit(sprites.sb_img, (res_b['s'][0]+mod, res_b['s'][1]))	
	for i in xrange(0, lamesa.rgn):
		mod = i*10
		SCREEN.blit(sprites.gn_img, (res_n['g'][0]+mod, res_n['g'][1]))	
	for i in xrange(0, lamesa.rgb):
		mod = i*10
		SCREEN.blit(sprites.gb_img, (res_b['g'][0]+mod, res_b['g'][1]))	
	for i in xrange(0, lamesa.rtn):
		mod = i*10
		SCREEN.blit(sprites.tn_img, (res_n['t'][0]+mod, res_n['t'][1]))	
	for i in xrange(0, lamesa.rtb):
		mod = i*10
		SCREEN.blit(sprites.tb_img, (res_b['t'][0]+mod, res_b['t'][1]))	
	for i in xrange(0, lamesa.rbn):
		mod = i*10
		SCREEN.blit(sprites.bn_img, (res_n['b'][0]+mod, res_n['b'][1]))	
	for i in xrange(0, lamesa.rbb):
		mod = i*10
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
	SCREEN.blit(sprites.kn_img, (lamesa.rey_n[0]-comp_n, lamesa.rey_n[1]-comp_n))
	SCREEN.blit(sprites.kb_img, (lamesa.rey_b[0]-comp_b, lamesa.rey_b[1]-comp_b))

#	reloj.tick(10)
	pygame.display.flip()
# una mas eficiente, que no actualiza la pantalla entera. busca sobre ésta:
# pygame.display.update()
