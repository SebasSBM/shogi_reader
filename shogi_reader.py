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

	Open the files in "games_recorded" directory to see how it works.
"""

import pygame, sys, re
from pygame.locals import *

pygame.init()
#reloj = pygame.time.Clock()
size = width, height = 1200,760

SCREEN = pygame.display.set_mode(size)
pygame.display.set_caption("ShogiReader - Reproductor de partidas grabadas")

# ******* TABLERO ********

r = 235
g = 220
b = 180

bg = int(r), int(g), int(b)

def redraw():
	SCREEN.fill(bg)

	#Verticals
	pygame.draw.line(SCREEN, (0,0,0), (20,20), (20,659))
	pygame.draw.line(SCREEN, (0,0,0), (91,20), (91,659))
	pygame.draw.line(SCREEN, (0,0,0), (162,20), (162,659))
	pygame.draw.line(SCREEN, (0,0,0), (233,20), (233,659))
	pygame.draw.line(SCREEN, (0,0,0), (304,20), (304,659))
	pygame.draw.line(SCREEN, (0,0,0), (375,20), (375,659))
	pygame.draw.line(SCREEN, (0,0,0), (446,20), (446,659))
	pygame.draw.line(SCREEN, (0,0,0), (517,20), (517,659))
	pygame.draw.line(SCREEN, (0,0,0), (588,20), (588,659))
	pygame.draw.line(SCREEN, (0,0,0), (659,20), (659,659))

	#Horizontals
	pygame.draw.line(SCREEN, (0,0,0), (20,20), (659,20))
	pygame.draw.line(SCREEN, (0,0,0), (20,91), (659,91))
	pygame.draw.line(SCREEN, (0,0,0), (20,162), (659,162))
	pygame.draw.line(SCREEN, (0,0,0), (20,233), (659,233))
	pygame.draw.line(SCREEN, (0,0,0), (20,304), (659,304))
	pygame.draw.line(SCREEN, (0,0,0), (20,375), (659,375))
	pygame.draw.line(SCREEN, (0,0,0), (20,446), (659,446))
	pygame.draw.line(SCREEN, (0,0,0), (20,517), (659,517))
	pygame.draw.line(SCREEN, (0,0,0), (20,588), (659,588))
	pygame.draw.line(SCREEN, (0,0,0), (20,659), (659,659))
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

# *** POSITIONS TABLE ***
coords_a = {
	'1': 589,
	'2': 518,
	'3': 447,
	'4': 376,
	'5': 305,
	'6': 234,
	'7': 163,
	'8': 92,
	'9': 21
}
coords_b = {
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

# *** Pieces arrays ***
lista_pn = {1:[589,447],2:[518,447],3:[447,447],4:[376,447],5:[305,447],6:[234,447],7:[163,447],8:[92,447],9:[21,447]}
lista_spn = {}
cnt_pn = 10
rpn = 0
lista_pb = {1:[589,163],2:[518,163],3:[447,163],4:[376,163],5:[305,163],6:[234,163],7:[163,163],8:[92,163],9:[21,163]}
lista_spb = {}
cnt_pb = 10
rpb = 0
lista_ln = {1:[21,589],2:[589,589]}
lista_sln = {}
cnt_ln = 3
rln = 0
lista_lb = {1:[21,21],2:[589,21]}
lista_slb = {}
cnt_lb = 3
rlb = 0
lista_nn = {1:[92,589],2:[518,589]}
lista_snn = {}
cnt_nn = 3
rnn = 0
lista_nb = {1:[92,21],2:[518,21]}
lista_snb = {}
cnt_nb = 3
rnb = 0
lista_sn = {1:[163,589],2:[447,589]}
lista_ssn = {}
cnt_sn = 3
rsn = 0
lista_sb = {1:[163,21],2:[447,21]}
lista_ssb = {}
cnt_sb = 3
rsb = 0
lista_gn = {1:[234,589],2:[376,589]}
cnt_gn = 3
rgn = 0
lista_gb = {1:[234,21],2:[376,21]}
cnt_gb = 3
rgb = 0
lista_tn = {1:[518,518]}
lista_stn = {}
cnt_tn = 2
rtn = 0
lista_tb = {1:[92,92]}
lista_stb = {}
cnt_tb = 2
rtb = 0
lista_bn = {1:[92,518]}
lista_sbn = {}
cnt_bn = 2
rbn = 0
lista_bb = {1:[518,92]}
lista_sbb = {}
cnt_bb = 2
rbb = 0
rey_n = [305,589]
rey_b = [305,21]

# *** Motion log array ***
history = []

# *** ALGORYTHM TO READ NOTATION AND TRANSFORM IT INTO DATA EXECUTABLE FORWARD AND BACKWARDS ***
import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()
partida = open(file_path, 'r')

#partida = open('hamshogi_victories/ibisha_vs_ibisha_mod.txt','r')
movs = partida.read().splitlines()
partida.close()

reg = re.compile('^\s*(\d+)-\s(.*)([-|x|\*])(.*)$')
for e in movs:
	kind = ''
	action = None
	promoting = False
	piece_respawn = ''
	piece_x = 0
	piece_y = 0
	frag = reg.match(e)
	destiny = [coords_a[frag.group(4)[0]],coords_b[frag.group(4)[1]]]
	if len(frag.group(4)) > 2:
		if frag.group(4)[2] == '+':
			promoting = True
	if (len(frag.group(2)) > 1 and frag.group(2)[0] != '+') or (len(frag.group(2)) > 2 and frag.group(2)[0] == '+'):
		if frag.group(2)[0] == '+':
			kind = frag.group(2)[0:2]
			piece_x = coords_a[frag.group(2)[2]]
			piece_y = coords_b[frag.group(2)[3]]
		else:
			kind = frag.group(2)[0]
			piece_x = coords_a[frag.group(2)[1]]
			piece_y = coords_b[frag.group(2)[2]]
	else:
		kind = frag.group(2)
	if frag.group(3) == 'x':
		action = 1
	elif frag.group(3) == '*':
		action = 2
	elif frag.group(3) == '-':
		action = 0

	if action == 1:
		if int(frag.group(1)) % 2 == 1: #Negras
			found = False
			while found == False:
				for k, e in lista_pb.items():
					if e == destiny:
						del lista_pb[k]
						rpn += 1
						piece_respawn = 'lista_pb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_spb.items():
					if e == destiny:
						del lista_spb[k]
						rpn += 1
						piece_respawn = 'lista_spb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_lb.items():
					if e == destiny:
						del lista_lb[k]
						rln += 1
						piece_respawn = 'lista_lb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_slb.items():
					if e == destiny:
						del lista_slb[k]
						rln += 1
						piece_respawn = 'lista_slb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_nb.items():
					if e == destiny:
						del lista_nb[k]
						rnn += 1
						piece_respawn = 'lista_nb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_snb.items():
					if e == destiny:
						del lista_snb[k]
						rnn += 1
						piece_respawn = 'lista_snb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_sb.items():
					if e == destiny:
						del lista_sb[k]
						rsn += 1
						piece_respawn = 'lista_sb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_ssb.items():
					if e == destiny:
						del lista_ssb[k]
						rsn += 1
						piece_respawn = 'lista_ssb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_gb.items():
					if e == destiny:
						del lista_gb[k]
						rgn += 1
						piece_respawn = 'lista_gb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_tb.items():
					if e == destiny:
						del lista_tb[k]
						rtn += 1
						piece_respawn = 'lista_tb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_stb.items():
					if e == destiny:
						del lista_stb[k]
						rtn += 1
						piece_respawn = 'lista_stb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_bb.items():
					if e == destiny:
						del lista_bb[k]
						rbn += 1
						piece_respawn = 'lista_bb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_sbb.items():
					if e == destiny:
						del lista_sbb[k]
						rbn += 1
						piece_respawn = 'lista_sbb['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
		else: # Blancas
			found = False
			while found == False:
				for k, e in lista_pn.items():
					if e == destiny:
						del lista_pn[k]
						rpb += 1
						piece_respawn = 'lista_pn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_spn.items():
					if e == destiny:
						del lista_spn[k]
						rpb += 1
						piece_respawn = 'lista_spn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_ln.items():
					if e == destiny:
						del lista_ln[k]
						rlb += 1
						piece_respawn = 'lista_ln['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_sln.items():
					if e == destiny:
						del lista_sln[k]
						rlb += 1
						piece_respawn = 'lista_sln['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_nn.items():
					if e == destiny:
						del lista_nn[k]
						rnb += 1
						piece_respawn = 'lista_nn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_snn.items():
					if e == destiny:
						del lista_snn[k]
						rnb += 1
						piece_respawn = 'lista_snn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_sn.items():
					if e == destiny:
						del lista_sn[k]
						rsb += 1
						piece_respawn = 'lista_sn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_ssn.items():
					if e == destiny:
						del lista_ssn[k]
						rsb += 1
						piece_respawn = 'lista_ssn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_gn.items():
					if e == destiny:
						del lista_gn[k]
						rgb += 1
						piece_respawn = 'lista_gn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_tn.items():
					if e == destiny:
						del lista_tn[k]
						rtb += 1
						piece_respawn = 'lista_tn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_stn.items():
					if e == destiny:
						del lista_stn[k]
						rtb += 1
						piece_respawn = 'lista_stn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_bn.items():
					if e == destiny:
						del lista_bn[k]
						rbb += 1
						piece_respawn = 'lista_bn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break
				if found == True:
					 break
				for k, e in lista_sbn.items():
					if e == destiny:
						del lista_sbn[k]
						rbb += 1
						piece_respawn = 'lista_sbn['+(str)(k)+']=['+(str)(e[0])+','+(str)(e[1])+']'
						found = True
						break


	if piece_x == 0 and action != 2:
		if int(frag.group(1)) % 2 == 1: #Negras
			if kind == 'P':
				for k, pn in lista_pn.items():
					if destiny[0] == pn[0] and destiny[1] == pn[1]-71:
						history.append(['lista_pn['+(str)(k)+']',[0,-71], action, promoting, piece_respawn])
						lista_pn[k] = destiny
						if promoting == True:
							del lista_pn[k]
							lista_spn[k] = destiny
						break
			if kind == 'L':
				for k, ln in lista_ln.items():
					if destiny[0] == ln[0] and destiny[1] < ln[1]:
						history.append(['lista_ln['+(str)(k)+']',[0,destiny[1]-ln[1]], action, promoting, piece_respawn])
						lista_ln[k] = destiny
						if promoting == True:
							del lista_ln[k]
							lista_sln[k] = destiny
						break
			if kind == 'N':
				for k, nn in lista_nn.items():
					if (destiny[0] == nn[0]+71 or destiny[0] == nn[0]-71 ) and destiny[1] == nn[1]-142:
						history.append(['lista_nn['+(str)(k)+']',[destiny[0]-nn[0],destiny[1]-nn[1]], action, promoting, piece_respawn])
						lista_nn[k] = destiny
						if promoting == True:
							del lista_nn[k]
							lista_snn[k] = destiny
						break
			if kind == 'S':
				for k, sn in lista_sn.items():
					if (destiny[0] <= sn[0]+71 and destiny[0] >= sn[0]-71 and destiny[1] == sn[1]-71) or ((destiny[0] == sn[0]+71 or destiny[0] == sn[0]-71) and destiny[1] == sn[1]+71):
						history.append(['lista_sn['+(str)(k)+']',[destiny[0]-sn[0],destiny[1]-sn[1]], action, promoting, piece_respawn])
						lista_sn[k] = destiny
						if promoting == True:
							del lista_sn[k]
							lista_ssn[k] = destiny
						break
			if kind == 'G':
				for k, gn in lista_gn.items():
					if (destiny[0] <= gn[0]+71 and destiny[0] >= gn[0]-71 and destiny[1] == gn[1]-71) or ((destiny[0] == gn[0]+71 or destiny[0] == gn[0]-71) and destiny[1] == gn[1]) or (destiny[0] == gn[0] and destiny[1] == gn[1]+71):
						history.append(['lista_gn['+(str)(k)+']',[destiny[0]-gn[0],destiny[1]-gn[1]], action, promoting, piece_respawn])
						lista_gn[k] = destiny
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lista_s'+mem+'n.items():\n\t'
				statem+= 'if (destiny[0] <= j[0]+71 and destiny[0] >= j[0]-71 and destiny[1] == j[1]-71) or ((destiny[0] == j[0]+71 or destiny[0] == j[0]-71) and destiny[1] == j[1]) or (destiny[0] == j[0] and destiny[1] == j[1]+71):\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'n["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',"'+piece_respawn+'"])\n\t\t'
				statem+= 'lista_s'+mem+'n[k] = destiny\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tn in lista_tn.items():
					if (destiny[0] == tn[0]) != (destiny[1] == tn[1]):
						history.append(['lista_tn['+(str)(k)+']',[destiny[0]-tn[0],destiny[1]-tn[1]], action, promoting, piece_respawn])
						lista_tn[k] = destiny
						if promoting == True:
							del lista_tn[k]
							lista_stn[k] = destiny
						break
			if kind == '+R':
				for k, stn in lista_stn.items():
					if ((destiny[0] == stn[0]) != (destiny[1] == stn[1])) or (destiny[0] <= stn[0]+71 and destiny[0] >= stn[0]-71 and destiny[1] <= stn[1]+71 and destiny[1] >= stn[1]-71):
						history.append(['lista_stn['+(str)(k)+']',[destiny[0]-stn[0],destiny[1]-stn[1]], action, promoting, piece_respawn])
						lista_stn[k] = destiny
						break
			if kind == 'B':
				for k, bn in lista_bn.items():
					if abs(destiny[0]-bn[0]) == abs(destiny[1]-bn[1]):
						history.append(['lista_bn['+(str)(k)+']',[destiny[0]-bn[0],destiny[1]-bn[1]], action, promoting, piece_respawn])
						lista_bn[k] = destiny
						if promoting == True:
							del lista_bn[k]
							lista_sbn[k] = destiny
						break
			if kind == '+B':
				for k, sbn in lista_sbn.items():
					if (abs(destiny[0]-sbn[0]) == abs(destiny[1]-sbn[1])) or (destiny[0] <= sbn[0]+71 and destiny[0] >= sbn[0]-71 and destiny[1] <= sbn[1]+71 and destiny[1] >= sbn[1]-71):
						history.append(['lista_sbn['+(str)(k)+']',[destiny[0]-sbn[0],destiny[1]-sbn[1]], action, promoting, piece_respawn])
						lista_sbn[k] = destiny
						break
			if kind == 'K':
				if destiny[0] <= rey_n[0]+71 and destiny[0] >= rey_n[0]-71 and destiny[1] <= rey_n[1]+71 and destiny[1] >= rey_n[1]-71:
					history.append(['rey_n',[destiny[0]-rey_n[0],destiny[1]-rey_n[1]], action, promoting, piece_respawn])
					rey_n = destiny
		else: #Blancas
			if kind == 'P':
				for k, pb in lista_pb.items():
					if destiny[0] == pb[0] and destiny[1] == pb[1]+71:
						history.append(['lista_pb['+(str)(k)+']',[0, 71], action, promoting, piece_respawn])
						lista_pb[k] = destiny
						if promoting == True:
							del lista_pb[k]
							lista_spb[k] = destiny
						break
			if kind == 'L':
				for k, lb in lista_lb.items():
					if destiny[0] == lb[0] and destiny[1] > lb[1]:
						history.append(['lista_lb['+(str)(k)+']',[0,destiny[1]-lb[1]], action, promoting, piece_respawn])
						lista_lb[k] = destiny
						if promoting == True:
							del lista_lb[k]
							lista_slb[k] = destiny
						break
			if kind == 'N':
				for k, nb in lista_nb.items():
					if (destiny[0] == nb[0]+71 or destiny[0] == nb[0]-71 ) and destiny[1] == nb[1]+142:
						history.append(['lista_nb['+(str)(k)+']',[destiny[0]-nb[0],destiny[1]-nb[1]], action, promoting, piece_respawn])
						lista_nb[k] = destiny
						if promoting == True:
							del lista_nb[k]
							lista_snb[k] = destiny
						break
			if kind == 'S':
				for k, sb in lista_sb.items():
					if (destiny[0] <= sb[0]+71 and destiny[0] >= sb[0]-71 and destiny[1] == sb[1]+71) or ((destiny[0] == sb[0]+71 or destiny[0] == sb[0]-71) and destiny[1] == sb[1]-71):
						history.append(['lista_sb['+(str)(k)+']',[destiny[0]-sb[0],destiny[1]-sb[1]], action, promoting, piece_respawn])
						lista_sb[k] = destiny
						if promoting == True:
							del lista_sb[k]
							lista_ssb[k] = destiny
						break
			if kind == 'G':
				for k, gb in lista_gb.items():
					if (destiny[0] <= gb[0]+71 and destiny[0] >= gb[0]-71 and destiny[1] == gb[1]+71) or ((destiny[0] == gb[0]+71 or destiny[0] == gb[0]-71) and destiny[1] == gb[1]) or (destiny[0] == gb[0] and destiny[1] == gb[1]-71):
						history.append(['lista_gb['+(str)(k)+']',[destiny[0]-gb[0],destiny[1]-gb[1]], action, promoting, piece_respawn])
						lista_gb[k] = destiny
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lista_s'+mem+'b.items():\n\t'
				statem+= 'if (destiny[0] <= j[0]+71 and destiny[0] >= j[0]-71 and destiny[1] == j[1]+71) or ((destiny[0] == j[0]+71 or destiny[0] == j[0]-71) and destiny[1] == j[1]) or (destiny[0] == j[0] and destiny[1] == j[1]-71):\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'b["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',"'+piece_respawn+'"])\n\t\t'
				statem+= 'lista_s'+mem+'b[k] = destiny\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tb in lista_tb.items():
					if (destiny[0] == tb[0]) != (destiny[1] == tb[1]):
						history.append(['lista_tb['+(str)(k)+']',[destiny[0]-tb[0],destiny[1]-tb[1]], action, promoting, piece_respawn])
						lista_tb[k] = destiny
						if promoting == True:
							del lista_tb[k]
							lista_stb[k] = destiny
						break
			if kind == '+R':
				for k, stb in lista_stb.items():
					if ((destiny[0] == stb[0]) != (destiny[1] == stb[1])) or (destiny[0] <= stb[0]+71 and destiny[0] >= stb[0]-71 and destiny[1] <= stb[1]+71 and destiny[1] >= stb[1]-71):
						history.append(['lista_stb['+(str)(k)+']',[destiny[0]-stb[0],destiny[1]-stb[1]], action, promoting, piece_respawn])
						lista_stb[k] = destiny
						break
			if kind == 'B':
				for k, bb in lista_bb.items():
					if abs(destiny[0]-bb[0]) == abs(destiny[1]-bb[1]):
						history.append(['lista_bb['+(str)(k)+']',[destiny[0]-bb[0],destiny[1]-bb[1]], action, promoting, piece_respawn])
						lista_bb[k] = destiny
						if promoting == True:
							del lista_bb[k]
							lista_sbb[k] = destiny
						break
			if kind == '+B':
				for k, sbb in lista_sbb.items():
					if (abs(destiny[0]-sbb[0]) == abs(destiny[1]-sbb[1])) or (destiny[0] <= sbb[0]+71 and destiny[0] >= sbb[0]-71 and destiny[1] <= sbb[1]+71 and destiny[1] >= sbb[1]-71):
						history.append(['lista_sbb['+(str)(k)+']',[destiny[0]-sbb[0],destiny[1]-sbb[1]], action, promoting, piece_respawn])
						lista_sbb[k] = destiny
						break
			if kind == 'K':
				if destiny[0] <= rey_b[0]+71 and destiny[0] >= rey_b[0]-71 and destiny[1] <= rey_b[1]+71 and destiny[1] >= rey_b[1]-71:
					history.append(['rey_b',[destiny[0]-rey_b[0],destiny[1]-rey_b[1]], action, promoting, piece_respawn])
					rey_b = destiny
	elif action != 2:
		if int(frag.group(1)) % 2 == 1: #Negras
			if kind == 'P':
				for k, pn in lista_pn.items():
					if pn[0] == piece_x and pn[1] == piece_y:
						history.append(['lista_pn['+(str)(k)+']',[0,-71], action, promoting, piece_respawn])
						lista_pn[k] = destiny
						if promoting == True:
							del lista_pn[k]
							lista_spn[k] = destiny
						break
			if kind == 'L':
				for k, ln in lista_ln.items():
					if ln[0] == piece_x and ln[1] == piece_y:
						history.append(['lista_ln['+(str)(k)+']',[0,destiny[1]-ln[1]], action, promoting, piece_respawn])
						lista_ln[k] = destiny
						if promoting == True:
							del lista_ln[k]
							lista_sln[k] = destiny
						break
			if kind == 'N':
				for k, nn in lista_nn.items():
					if nn[0] == piece_x and nn[1] == piece_y:
						history.append(['lista_nn['+(str)(k)+']',[destiny[0]-nn[0],destiny[1]-nn[1]], action, promoting, piece_respawn])
						lista_nn[k] = destiny
						if promoting == True:
							del lista_nn[k]
							lista_snn[k] = destiny
						break
			if kind == 'S':
				for k, sn in lista_sn.items():
					if sn[0] == piece_x and sn[1] == piece_y:
						history.append(['lista_sn['+(str)(k)+']',[destiny[0]-sn[0],destiny[1]-sn[1]], action, promoting, piece_respawn])
						lista_sn[k] = destiny
						if promoting == True:
							del lista_sn[k]
							lista_ssn[k] = destiny
						break
			if kind == 'G':
				for k, gn in lista_gn.items():
					if gn[0] == piece_x and gn[1] == piece_y:
						history.append(['lista_gn['+(str)(k)+']',[destiny[0]-gn[0],destiny[1]-gn[1]], action, promoting, piece_respawn])
						lista_gn[k] = destiny
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lista_s'+mem+'n.items():\n\t'
				statem+= 'if j[0] == piece_x and j[1] == piece_y:\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'n["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',"'+piece_respawn+'"])\n\t\t'
				statem+= 'lista_s'+mem+'n[k] = destiny\n\t\t'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tn in lista_tn.items():
					if tn[0] == piece_x and tn[1] == piece_y:
						history.append(['lista_tn['+(str)(k)+']',[destiny[0]-tn[0],destiny[1]-tn[1]], action, promoting, piece_respawn])
						lista_tn[k] = destiny
						if promoting == True:
							del lista_tn[k]
							lista_stn[k] = destiny
						break
			if kind == '+R':
				for k, stn in lista_stn.items():
					if stn[0] == piece_x and stn[1] == piece_y:
						history.append(['lista_stn['+(str)(k)+']',[destiny[0]-stn[0],destiny[1]-stn[1]], action, promoting, piece_respawn])
						lista_stn[k] = destiny
						break
			if kind == 'B':
				for k, bn in lista_bn.items():
					if bn[0] == piece_x and bn[1] == piece_y:
						history.append(['lista_bn['+(str)(k)+']',[destiny[0]-bn[0],destiny[1]-bn[1]], action, promoting, piece_respawn])
						lista_bn[k] = destiny
						if promoting == True:
							del lista_bn[k]
							lista_sbn[k] = destiny
						break
			if kind == '+B':
				for k, sbn in lista_sbn.items():
					if sbn[0] == piece_x and sbn[1] == piece_y:
						history.append(['lista_sbn['+(str)(k)+']',[destiny[0]-sbn[0],destiny[1]-sbn[1]], action, promoting, piece_respawn])
						lista_sbn[k] = destiny
						break
		else: # Blancas
			if kind == 'P':
				for k, pb in lista_pb.items():
					if pb[0] == piece_x and pb[1] == piece_y:
						history.append(['lista_pb['+(str)(k)+']',[0,+71], action, promoting, piece_respawn])
						lista_pb[k] = destiny
						if promoting == True:
							del lista_pb[k]
							lista_spb[k] = destiny
						break
			if kind == 'L':
				for k, lb in lista_lb.items():
					if lb[0] == piece_x and lb[1] == piece_y:
						history.append(['lista_lb['+(str)(k)+']',[0,destiny[1]-lb[1]], action, promoting, piece_respawn])
						lista_lb[k] = destiny
						if promoting == True:
							del lista_lb[k]
							lista_slb[k] = destiny
						break
			if kind == 'N':
				for k, nb in lista_nb.items():
					if nb[0] == piece_x and nb[1] == piece_y:
						history.append(['lista_nb['+(str)(k)+']',[destiny[0]-nb[0],destiny[1]-nb[1]], action, promoting, piece_respawn])
						lista_nb[k] = destiny
						if promoting == True:
							del lista_nb[k]
							lista_snb[k] = destiny
						break
			if kind == 'S':
				for k, sb in lista_sb.items():
					if sb[0] == piece_x and sb[1] == piece_y:
						history.append(['lista_sb['+(str)(k)+']',[destiny[0]-sb[0],destiny[1]-sb[1]], action, promoting, piece_respawn])
						lista_sb[k] = destiny
						if promoting == True:
							del lista_sb[k]
							lista_ssb[k] = destiny
						break
			if kind == 'G':
				for k, gb in lista_gb.items():
					if gb[0] == piece_x and gb[1] == piece_y:
						history.append(['lista_gb['+(str)(k)+']',[destiny[0]-gb[0],destiny[1]-gb[1]], action, promoting, piece_respawn])
						lista_gb[k] = destiny
						break
			if kind == '+P' or kind == '+L' or kind == '+N' or kind == '+S':
				mem = kind[1].lower()
				statem = 'for k, j in lista_s'+mem+'n.items():\n\t'
				statem+= 'if j[0] == piece_x and j[1] == piece_y:\n\t\t'
				statem+= 'history.append(["lista_s'+mem+'b["+(str)(k)+"]",[destiny[0]-j[0],destiny[1]-j[1]],'+(str)(action)+','+(str)(promoting)+',"'+piece_respawn+'"])\n\t\t'
				statem+= 'lista_s'+mem+'b[k] = destiny'
				statem+= 'break'
				exec statem
			if kind == 'R':
				for k, tb in lista_tb.items():
					if tb[0] == piece_x and tb[1] == piece_y:
						history.append(['lista_tb['+(str)(k)+']',[destiny[0]-tb[0],destiny[1]-tb[1]], action, promoting, piece_respawn])
						lista_tb[k] = destiny
						if promoting == True:
							del lista_tb[k]
							lista_stb[k] = destiny
						break
			if kind == '+R':
				for k, stb in lista_stb.items():
					if stb[0] == piece_x and stb[1] == piece_y:
						history.append(['lista_stb['+(str)(k)+']',[destiny[0]-stb[0],destiny[1]-stb[1]], action, promoting, piece_respawn])
						lista_stb[k] = destiny
						break
			if kind == 'B':
				for k, bb in lista_bb.items():
					if bb[0] == piece_x and bb[1] == piece_y:
						history.append(['lista_bb['+(str)(k)+']',[destiny[0]-bb[0],destiny[1]-bb[1]], action, promoting, piece_respawn])
						lista_bb[k] = destiny
						if promoting == True:
							del lista_bb[k]
							lista_sbb[k] = destiny
						break
			if kind == '+B':
				for k, sbb in lista_sbb.items():
					if sbb[0] == piece_x and sbb[1] == piece_y:
						history.append(['lista_sbb['+(str)(k)+']',[destiny[0]-sbb[0],destiny[1]-sbb[1]], action, promoting, piece_respawn])
						lista_sbb[k] = destiny
						break
	else: # Action=2 (reingreso)
		if int(frag.group(1)) % 2 == 1: #Negras
			player = 'n'
		else:
			player = 'b'

		if kind == 'P':
			if player == 'n':
				history.append([['pn',cnt_pn], destiny, action, promoting, piece_respawn])	
				lista_pn[cnt_pn] = destiny
				cnt_pn += 1
				rpn -= 1
			else:
				history.append([['pb',cnt_pb], destiny, action, promoting, piece_respawn])	
				lista_pb[cnt_pb] = destiny
				cnt_pb += 1
				rpb -= 1
		if kind == 'L':
			if player == 'n':
				history.append([['ln',cnt_ln], destiny, action, promoting, piece_respawn])
				lista_ln[cnt_ln] = destiny
				cnt_ln += 1
				rln -= 1
			else:
				history.append([['lb',cnt_lb], destiny, action, promoting, piece_respawn])
				lista_lb[cnt_lb] = destiny
				cnt_lb += 1
				rlb -= 1
		if kind == 'N':
			if player == 'n':
				history.append([['nn',cnt_nn], destiny, action, promoting, piece_respawn])
				lista_nn[cnt_nn] = destiny
				cnt_nn += 1
				rnn -= 1
			else:
				history.append([['nb',cnt_nb], destiny, action, promoting, piece_respawn])
				lista_nb[cnt_nb] = destiny
				cnt_nb += 1
				rnb -= 1
		if kind == 'S':
			if player == 'n':
				history.append([['sn',cnt_sn], destiny, action, promoting, piece_respawn])
				lista_sn[cnt_sn] = destiny
				cnt_sn += 1
				rsn -= 1
			else:
				history.append([['sb',cnt_sb], destiny, action, promoting, piece_respawn])
				lista_sb[cnt_sb] = destiny
				cnt_sb += 1
				rsb -= 1
		if kind == 'G':
			if player == 'n':
				history.append([['gn',cnt_gn], destiny, action, promoting, piece_respawn])
				lista_gn[cnt_gn] = destiny
				cnt_gn += 1
				rgn -= 1
			else:
				history.append([['gb',cnt_gb], destiny, action, promoting, piece_respawn])
				lista_gb[cnt_gb] = destiny
				cnt_gb += 1
				rgb -= 1
		if kind == 'R':
			if player == 'n':
				history.append([['tn',cnt_tn], destiny, action, promoting, piece_respawn])
				lista_tn[cnt_tn] = destiny
				cnt_tn += 1
				rtn -= 1
			else:
				history.append([['tb',cnt_tb], destiny, action, promoting, piece_respawn])
				lista_tb[cnt_tb] = destiny
				cnt_tb += 1
				rtb -= 1
		if kind == 'B':
			if player == 'n':
				history.append([['bn',cnt_bn], destiny, action, promoting, piece_respawn])
				lista_bn[cnt_bn] = destiny
				cnt_bn += 1
				rbn -= 1
			else:
				history.append([['bb',cnt_bb], destiny, action, promoting, piece_respawn])
				lista_bb[cnt_bb] = destiny
				cnt_bb += 1
				rbb -= 1

	#Loading progress
	#print len(history)

# *** sprites ***
pawn_probe = pygame.image.load("ShogiSprites/Peon.png")
pn_img = pygame.transform.scale(pawn_probe, (70,70))
pb_img = pygame.transform.rotozoom(pn_img, 180, 1)

spawn_probe = pygame.image.load("ShogiSprites/SPeon.png")
spn_img = pygame.transform.scale(spawn_probe, (70,70))
spb_img = pygame.transform.rotozoom(spn_img, 180, 1)

lance_probe = pygame.image.load("ShogiSprites/Lanza.png")
ln_img = pygame.transform.scale(lance_probe, (70,70))
lb_img = pygame.transform.rotozoom(ln_img, 180, 1)

slance_probe = pygame.image.load("ShogiSprites/SLanza.png")
sln_img = pygame.transform.scale(slance_probe, (70,70))
slb_img = pygame.transform.rotozoom(sln_img, 180, 1)

knight_probe = pygame.image.load("ShogiSprites/Caballo.png")
nn_img = pygame.transform.scale(knight_probe, (70,70))
nb_img = pygame.transform.rotozoom(nn_img, 180, 1)

sknight_probe = pygame.image.load("ShogiSprites/SCaballo.png")
snn_img = pygame.transform.scale(sknight_probe, (70,70))
snb_img = pygame.transform.rotozoom(snn_img, 180, 1)

silver_probe = pygame.image.load("ShogiSprites/Plata.png")
sn_img = pygame.transform.scale(silver_probe, (70,70))
sb_img = pygame.transform.rotozoom(sn_img, 180, 1)

ssilver_probe = pygame.image.load("ShogiSprites/SPlata.png")
ssn_img = pygame.transform.scale(ssilver_probe, (70,70))
ssb_img = pygame.transform.rotozoom(ssn_img, 180, 1)

gold_probe = pygame.image.load("ShogiSprites/Oro.png")
gn_img = pygame.transform.scale(gold_probe, (70,70))
gb_img = pygame.transform.rotozoom(gn_img, 180, 1)

tower_probe = pygame.image.load("ShogiSprites/Torre.png")
tn_img = pygame.transform.scale(tower_probe, (70,70))
tb_img = pygame.transform.rotozoom(tn_img, 180, 1)

stower_probe = pygame.image.load("ShogiSprites/STorre.png")
stn_img = pygame.transform.scale(stower_probe, (70,70))
stb_img = pygame.transform.rotozoom(stn_img, 180, 1)

bishop_probe = pygame.image.load("ShogiSprites/Alfil.png")
bn_img = pygame.transform.scale(bishop_probe, (70,70))
bb_img = pygame.transform.rotozoom(bn_img, 180, 1)

sbishop_probe = pygame.image.load("ShogiSprites/SAlfil.png")
sbn_img = pygame.transform.scale(sbishop_probe, (70,70))
sbb_img = pygame.transform.rotozoom(sbn_img, 180, 1)

kingn_probe = pygame.image.load("ShogiSprites/ReyN.png")
kn_img = pygame.transform.scale(kingn_probe, (70,70))

kingb_probe = pygame.image.load("ShogiSprites/ReyB.png")
kb_img = pygame.transform.scale(kingb_probe, (70,70))
kb_img = pygame.transform.rotozoom(kb_img, 180, 1)

pos = 0
max_history = len(history)

#TODO:
#   History registries should be optimized to prevent the mess in move_forward() 
# and move backwards() to handle some extraordinary situations. When I say "mess"
# I mean that some instructions are excessively complicated I guess, they are doing
# thing that I'm sure can be achieved in a more simple way.

def move_forward():
	global pos
	if history[pos][2] == 2:
		#In this case,
		# history[pos] structure -> [[kind_of_piece,counter_to_assign_id], destiny_coords, action, promoting, piece_respawn]
		statem = 'lista_'+history[pos][0][0]+'['+(str)(history[pos][0][1])+']=['+(str)(history[pos][1][0])+','+(str)(history[pos][1][1])+']'
		exec statem
		statem = 'r'+history[pos][0][0]+'-=1'
		exec statem
	else:
		# Standard case,
		# history[pos] structure -> [code_statement_to_select_piece, coords_sum, action, promoting, piece_respawn]
		statem = history[pos][0]+'[0]+='+(str)(history[pos][1][0])
		exec statem
		statem = history[pos][0]+'[1]+='+(str)(history[pos][1][1])
		exec statem
		if history[pos][3] == True: #Handle piece_promotion==True
			#TODO Simplify this task avoiding the regexp abuse
			prueba = re.match('^.*\[(.*)\]$', history[pos][0])
			statem = 'prueba2='+history[pos][0]
			exec statem
			statem = 'del '+history[pos][0]
			exec statem
			prueba4 = re.match('^.*_(.*)\[.*\]$', history[pos][0])
			statem = 'lista_s'+prueba4.group(1)+'['+prueba.group(1)+']=['+(str)(prueba2[0])+','+(str)(prueba2[1])+']'
			exec statem
	if history[pos][4] != '':#Piece captured that has to be respawn backwards
		# TODO Avoid regexp abuse
		frag = re.match('^(lista_.*\[.*\])=\[.*,.*\]$', history[pos][4])
		theobj = frag.group(1)
		statem = 'del '+theobj
		exec statem
	pos += 1
	previous_highlight(pos)

def previous_highlight(cursor):
	#TODO Current piece must also be highlighted
	global history, SCREEN
	if cursor > 0:
		if history[cursor-1][2] != 2:
			obj = history[cursor-1][0]
			if history[cursor-1][3] == True:
				frag = re.match('^lista_(.*\[.*\])$', obj)
				obj = 'lista_s'+frag.group(1)
			statem = 'coords='+obj
			exec statem
			drawcoords = [coords[0]-history[cursor-1][1][0],coords[1]-history[cursor-1][1][1]]
			pygame.draw.rect(SCREEN, (0,255,0), (drawcoords[0], drawcoords[1], 70, 70))
			
	
def move_back():
	global pos
	pos -= 1
	if history[pos][2] == 2:
		statem = 'del lista_'+history[pos][0][0]+'['+(str)(history[pos][0][1])+']'
		exec statem
		statem = 'r'+history[pos][0][0]+'+=1'
		exec statem
	else:
		if history[pos][3] == True:
			#TODO Avoid regexp abuse
			prueba = re.match('^.*\[(.*)\]$', history[pos][0])
			prueba4 = re.match('^.*_(.*)\[.*\]$', history[pos][0])
			statem = 'prueba2=lista_s'+prueba4.group(1)+'['+prueba.group(1)+']'
			exec statem
			statem = history[pos][0]+'=['+(str)(prueba2[0])+','+(str)(prueba2[1])+']'
			exec statem
			statem = 'del lista_s'+prueba4.group(1)+'['+prueba.group(1)+']'
			exec statem
		statem = history[pos][0]+'[0]-='+(str)(history[pos][1][0])
		exec statem
		statem = history[pos][0]+'[1]-='+(str)(history[pos][1][1])
		exec statem
	if history[pos][4] != '':
		exec history[pos][4]
	previous_highlight(pos)

# TODO Avoid this code duplicate (for instance, enclosing this setup in a function)
# *** Pieces arrays *** -> restart
lista_pn = {1:[589,447],2:[518,447],3:[447,447],4:[376,447],5:[305,447],6:[234,447],7:[163,447],8:[92,447],9:[21,447]}
lista_spn = {}
cnt_pn = 10
rpn = 0
lista_pb = {1:[589,163],2:[518,163],3:[447,163],4:[376,163],5:[305,163],6:[234,163],7:[163,163],8:[92,163],9:[21,163]}
lista_spb = {}
cnt_pb = 10
rpb = 0
lista_ln = {1:[21,589],2:[589,589]}
lista_sln = {}
cnt_ln = 3
rln = 0
lista_lb = {1:[21,21],2:[589,21]}
lista_slb = {}
cnt_lb = 3
rlb = 0
lista_nn = {1:[92,589],2:[518,589]}
lista_snn = {}
cnt_nn = 3
rnn = 0
lista_nb = {1:[92,21],2:[518,21]}
lista_snb = {}
cnt_nb = 3
rnb = 0
lista_sn = {1:[163,589],2:[447,589]}
lista_ssn = {}
cnt_sn = 3
rsn = 0
lista_sb = {1:[163,21],2:[447,21]}
lista_ssb = {}
cnt_sb = 3
rsb = 0
lista_gn = {1:[234,589],2:[376,589]}
cnt_gn = 3
rgn = 0
lista_gb = {1:[234,21],2:[376,21]}
cnt_gb = 3
rgb = 0
lista_tn = {1:[518,518]}
lista_stn = {}
cnt_tn = 2
rtn = 0
lista_tb = {1:[92,92]}
lista_stb = {}
cnt_tb = 2
rtb = 0
lista_bn = {1:[92,518]}
lista_sbn = {}
cnt_bn = 2
rbn = 0
lista_bb = {1:[518,92]}
lista_sbb = {}
cnt_bb = 2
rbb = 0
rey_n = [305,589]
rey_b = [305,21]

cnt_fw = 0
cnt_bw = 0
hold_fw = False
hold_bw = False
delay = 10
while True:
#	pygame.draw.rect(SCREEN, (0,255,0), (305, 305, 70, 70))
	# Hold mode
	if hold_fw:
		cnt_fw += 1
		if cnt_fw >= 10 and pos < max_history:
			redraw()
			move_forward()
	if hold_bw:
		cnt_bw += 1
		if cnt_bw >= 10 and pos > 0:
			redraw()
			move_back()

	# Optimizing CPU consumption
	event = pygame.event.wait()
#	for event in pygame.event.get():
	if event.type == pygame.QUIT:
		sys.exit()
	elif event.type == KEYDOWN and event.key == K_ESCAPE:
		sys.exit()
	elif event.type == KEYDOWN and event.key == K_d and pos < max_history:
		redraw()
		move_forward()
		hold_fw = True
		if cnt_fw < 10:
			cnt_fw += 1
	elif event.type == KEYUP and event.key == K_d:
		hold_fw = False
		cnt_fw = 0
	elif event.type == KEYDOWN and event.key == K_a and pos > 0:
		redraw()
		move_back()
		hold_bw = True
		if cnt_bw < 10:
			cnt_bw += 1
	elif event.type == KEYUP and event.key == K_a:
		hold_bw = False
		cnt_bw = 0

#		elif event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
#			silent.play()
#		elif event.type == KEYDOWN and event.key == K_SPACE:
#			pygame.image.save(screen, "screenshot.png")

	mx,my = pygame.mouse.get_pos()
#	pygame.draw.line(SCREEN, (0,0,0), (20,20), (mx,my))

	# *** This reads the current position of pieces to place them ***

	for k, pn in lista_pn.items():
		SCREEN.blit(pn_img, pn)
	for k, spn in lista_spn.items():
		SCREEN.blit(spn_img, spn)
	for k, pb in lista_pb.items():
		SCREEN.blit(pb_img, (pb[0]-2, pb[1]-2))
	for k, spb in lista_spb.items():
		SCREEN.blit(spb_img, (spb[0]-2, spb[1]-2))
	for k, ln in lista_ln.items():
		SCREEN.blit(ln_img, ln)
	for k, sln in lista_sln.items():
		SCREEN.blit(sln_img, sln)
	for k, lb in lista_lb.items():
		SCREEN.blit(lb_img, (lb[0]-2, lb[1]-2))
	for k, slb in lista_slb.items():
		SCREEN.blit(slb_img, (slb[0]-2, slb[1]-2))
	for k, nn in lista_nn.items():
		SCREEN.blit(nn_img, nn)
	for k, snn in lista_snn.items():
		SCREEN.blit(snn_img, snn)
	for k, nb in lista_nb.items():
		SCREEN.blit(nb_img, (nb[0]-2, nb[1]-2))
	for k, snb in lista_snb.items():
		SCREEN.blit(snb_img, (snb[0]-2, snb[1]-2))
	for k, sn in lista_sn.items():
		SCREEN.blit(sn_img, sn)
	for k, ssn in lista_ssn.items():
		SCREEN.blit(ssn_img, ssn)
	for k, sb in lista_sb.items():
		SCREEN.blit(sb_img, (sb[0]-2, sb[1]-2))
	for k, ssb in lista_ssb.items():
		SCREEN.blit(ssb_img, (ssb[0]-2, ssb[1]-2))
	for k, gn in lista_gn.items():
		SCREEN.blit(gn_img, gn)
	for k, gb in lista_gb.items():
		SCREEN.blit(gb_img, (gb[0]-2, gb[1]-2))
	for k, tn in lista_tn.items():
		SCREEN.blit(tn_img, tn)
	for k, stn in lista_stn.items():
		SCREEN.blit(stn_img, stn)
	for k, tb in lista_tb.items():
		SCREEN.blit(tb_img, (tb[0]-2, tb[1]-2))
	for k, stb in lista_stb.items():
		SCREEN.blit(stb_img, (stb[0]-2, stb[1]-2))
	for k, bn in lista_bn.items():
		SCREEN.blit(bn_img, bn)
	for k, sbn in lista_sbn.items():
		SCREEN.blit(sbn_img, sbn)
	for k, bb in lista_bb.items():
		SCREEN.blit(bb_img, (bb[0]-2, bb[1]-2))
	for k, sbb in lista_sbb.items():
		SCREEN.blit(sbb_img, (sbb[0]-2, sbb[1]-2))
	SCREEN.blit(kn_img, rey_n)
	SCREEN.blit(kb_img, (rey_b[0]-2,rey_b[1]-2))

#	reloj.tick(10)
	pygame.display.flip()
# una mas eficiente, que no actualiza la pantalla entera. busca sobre ésta:
# pygame.display.update()
