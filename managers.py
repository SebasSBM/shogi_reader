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
	This file contains the classes defined for shogi_reader
"""
import pygame, re, tkMessageBox

class coords_manager:
	def __init__(self):
		# Pieces arrays
		self.lista_pn = None
		self.lista_spn = None
		self.cnt_pn = None
		self.rpn = None
		self.lista_pb = None
		self.lista_spb = None
		self.cnt_pb = None
		self.rpb = None
		self.lista_ln = None
		self.lista_sln = None
		self.cnt_ln = None
		self.rln = None
		self.lista_lb = None
		self.lista_slb = None
		self.cnt_lb = None
		self.rlb = None
		self.lista_nn = None
		self.lista_snn = None
		self.cnt_nn = None
		self.rnn = None
		self.lista_nb = None
		self.lista_snb = None
		self.cnt_nb = None
		self.rnb = None
		self.lista_sn = None
		self.lista_ssn = None
		self.cnt_sn = None
		self.rsn = None
		self.lista_sb = None
		self.lista_ssb = None
		self.cnt_sb = None
		self.rsb = None
		self.lista_gn = None
		self.cnt_gn = None
		self.rgn = None
		self.lista_gb = None
		self.cnt_gb = None
		self.rgb = None
		self.lista_tn = None
		self.lista_stn = None
		self.cnt_tn = None
		self.rtn = None
		self.lista_tb = None
		self.lista_stb = None
		self.cnt_tb = None
		self.rtb = None
		self.lista_bn = None
		self.lista_sbn = None
		self.cnt_bn = None
		self.rbn = None
		self.lista_bb = None
		self.lista_sbb = None
		self.cnt_bb = None
		self.rbb = None
		self.rey_n = None
		self.rey_b = None

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
		self.lista_pn = {1:[self.coords_x['1'],self.coords_y['g']],2:[self.coords_x['2'],self.coords_y['g']],3:[self.coords_x['3'],self.coords_y['g']],4:[self.coords_x['4'],self.coords_y['g']],5:[self.coords_x['5'],self.coords_y['g']],6:[self.coords_x['6'],self.coords_y['g']],7:[self.coords_x['7'],self.coords_y['g']],8:[self.coords_x['8'],self.coords_y['g']],9:[self.coords_x['9'],self.coords_y['g']]}
		self.lista_spn = {}
		self.cnt_pn = 10
		self.rpn = 0
		self.lista_pb = {1:[self.coords_x['1'],self.coords_y['c']],2:[self.coords_x['2'],self.coords_y['c']],3:[self.coords_x['3'],self.coords_y['c']],4:[self.coords_x['4'],self.coords_y['c']],5:[self.coords_x['5'],self.coords_y['c']],6:[self.coords_x['6'],self.coords_y['c']],7:[self.coords_x['7'],self.coords_y['c']],8:[self.coords_x['8'],self.coords_y['c']],9:[self.coords_x['9'],self.coords_y['c']]}
		self.lista_spb = {}
		self.cnt_pb = 10
		self.rpb = 0
		self.lista_ln = {1:[self.coords_x['1'],self.coords_y['i']],2:[self.coords_x['9'],self.coords_y['i']]}
		self.lista_sln = {}
		self.cnt_ln = 3
		self.rln = 0
		self.lista_lb = {1:[self.coords_x['1'],self.coords_y['a']],2:[self.coords_x['9'],self.coords_y['a']]}
		self.lista_slb = {}
		self.cnt_lb = 3
		self.rlb = 0
		self.lista_nn = {1:[self.coords_x['2'],self.coords_y['i']],2:[self.coords_x['8'],self.coords_y['i']]}
		self.lista_snn = {}
		self.cnt_nn = 3
		self.rnn = 0
		self.lista_nb = {1:[self.coords_x['2'],self.coords_y['a']],2:[self.coords_x['8'],self.coords_y['a']]}
		self.lista_snb = {}
		self.cnt_nb = 3
		self.rnb = 0
		self.lista_sn = {1:[self.coords_x['3'],self.coords_y['i']],2:[self.coords_x['7'],self.coords_y['i']]}
		self.lista_ssn = {}
		self.cnt_sn = 3
		self.rsn = 0
		self.lista_sb = {1:[self.coords_x['3'],self.coords_y['a']],2:[self.coords_x['7'],self.coords_y['a']]}
		self.lista_ssb = {}
		self.cnt_sb = 3
		self.rsb = 0
		self.lista_gn = {1:[self.coords_x['4'],self.coords_y['i']],2:[self.coords_x['6'],self.coords_y['i']]}
		self.cnt_gn = 3
		self.rgn = 0
		self.lista_gb = {1:[self.coords_x['4'],self.coords_y['a']],2:[self.coords_x['6'],self.coords_y['a']]}
		self.cnt_gb = 3
		self.rgb = 0
		self.lista_tn = {1:[self.coords_x['2'],self.coords_y['h']]}
		self.lista_stn = {}
		self.cnt_tn = 2
		self.rtn = 0
		self.lista_tb = {1:[self.coords_x['8'],self.coords_y['b']]}
		self.lista_stb = {}
		self.cnt_tb = 2
		self.rtb = 0
		self.lista_bn = {1:[self.coords_x['8'],self.coords_y['h']]}
		self.lista_sbn = {}
		self.cnt_bn = 2
		self.rbn = 0
		self.lista_bb = {1:[self.coords_x['2'],self.coords_y['b']]}
		self.lista_sbb = {}
		self.cnt_bb = 2
		self.rbb = 0
		self.rey_n = [self.coords_x['5'],self.coords_y['i']]
		self.rey_b = [self.coords_x['5'],self.coords_y['a']]

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
		for k, e in self.lista_pn.items():
			self.lista_pn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_spn.items():
			self.lista_spn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_pb.items():
			self.lista_pb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_spb.items():
			self.lista_spb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_ln.items():
			self.lista_ln[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_sln.items():
			self.lista_sln[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_lb.items():
			self.lista_lb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_slb.items():
			self.lista_slb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_nn.items():
			self.lista_nn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_snn.items():
			self.lista_snn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_nb.items():
			self.lista_nb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_snb.items():
			self.lista_snb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_sn.items():
			self.lista_sn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_ssn.items():
			self.lista_ssn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_sb.items():
			self.lista_sb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_ssb.items():
			self.lista_ssb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_gn.items():
			self.lista_gn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_gb.items():
			self.lista_gb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_tn.items():
			self.lista_tn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_stn.items():
			self.lista_stn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_tb.items():
			self.lista_tb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_stb.items():
			self.lista_stb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_bn.items():
			self.lista_bn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_sbn.items():
			self.lista_sbn[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_bb.items():
			self.lista_bb[k] = [revert_x[e[0]],revert_y[e[1]]]
		for k, e in self.lista_sbb.items():
			self.lista_sbb[k] = [revert_x[e[0]],revert_y[e[1]]]
		self.rey_n = [revert_x[self.rey_n[0]],revert_y[self.rey_n[1]]]
		self.rey_b = [revert_x[self.rey_b[0]],revert_y[self.rey_b[1]]]
		
		self.update()

class sprites_manager:
	def __init__(self):
		self.pawn_probe = pygame.image.load("ShogiSprites/Peon.png")
		self.pn_img = None
		self.pb_img = None

		self.spawn_probe = pygame.image.load("ShogiSprites/SPeon.png")
		self.spn_img = None
		self.spb_img = None

		self.lance_probe = pygame.image.load("ShogiSprites/Lanza.png")
		self.ln_img = None
		self.lb_img = None

		self.slance_probe = pygame.image.load("ShogiSprites/SLanza.png")
		self.sln_img = None
		self.slb_img = None

		self.knight_probe = pygame.image.load("ShogiSprites/Caballo.png")
		self.nn_img = None
		self.nb_img = None

		self.sknight_probe = pygame.image.load("ShogiSprites/SCaballo.png")
		self.snn_img = None
		self.snb_img = None

		self.silver_probe = pygame.image.load("ShogiSprites/Plata.png")
		self.sn_img = None
		self.sb_img = None

		self.ssilver_probe = pygame.image.load("ShogiSprites/SPlata.png")
		self.ssn_img = None
		self.ssb_img = None

		self.gold_probe = pygame.image.load("ShogiSprites/Oro.png")
		self.gn_img = None
		self.gb_img = None

		self.tower_probe = pygame.image.load("ShogiSprites/Torre.png")
		self.tn_img = None
		self.tb_img = None

		self.stower_probe = pygame.image.load("ShogiSprites/STorre.png")
		self.stn_img = None
		self.stb_img = None

		self.bishop_probe = pygame.image.load("ShogiSprites/Alfil.png")
		self.bn_img = None
		self.bb_img = None

		self.sbishop_probe = pygame.image.load("ShogiSprites/SAlfil.png")
		self.sbn_img = None
		self.sbb_img = None

		self.kingn_probe = pygame.image.load("ShogiSprites/ReyN.png")
		self.kn_img = None

		self.kingb_probe = pygame.image.load("ShogiSprites/ReyB.png")
		self.kb_img = None
		self.revert(1)

	def revert(self, state):
		if state == 1:
			self.pn_img = pygame.transform.scale(self.pawn_probe, (70,70))
			self.pb_img = pygame.transform.rotozoom(self.pn_img, 180, 1)

			self.spn_img = pygame.transform.scale(self.spawn_probe, (70,70))
			self.spb_img = pygame.transform.rotozoom(self.spn_img, 180, 1)

			self.ln_img = pygame.transform.scale(self.lance_probe, (70,70))
			self.lb_img = pygame.transform.rotozoom(self.ln_img, 180, 1)

			self.sln_img = pygame.transform.scale(self.slance_probe, (70,70))
			self.slb_img = pygame.transform.rotozoom(self.sln_img, 180, 1)

			self.nn_img = pygame.transform.scale(self.knight_probe, (70,70))
			self.nb_img = pygame.transform.rotozoom(self.nn_img, 180, 1)

			self.snn_img = pygame.transform.scale(self.sknight_probe, (70,70))
			self.snb_img = pygame.transform.rotozoom(self.snn_img, 180, 1)

			self.sn_img = pygame.transform.scale(self.silver_probe, (70,70))
			self.sb_img = pygame.transform.rotozoom(self.sn_img, 180, 1)

			self.ssn_img = pygame.transform.scale(self.ssilver_probe, (70,70))
			self.ssb_img = pygame.transform.rotozoom(self.ssn_img, 180, 1)

			self.gn_img = pygame.transform.scale(self.gold_probe, (70,70))
			self.gb_img = pygame.transform.rotozoom(self.gn_img, 180, 1)

			self.tn_img = pygame.transform.scale(self.tower_probe, (70,70))
			self.tb_img = pygame.transform.rotozoom(self.tn_img, 180, 1)

			self.stn_img = pygame.transform.scale(self.stower_probe, (70,70))
			self.stb_img = pygame.transform.rotozoom(self.stn_img, 180, 1)

			self.bn_img = pygame.transform.scale(self.bishop_probe, (70,70))
			self.bb_img = pygame.transform.rotozoom(self.bn_img, 180, 1)

			self.sbn_img = pygame.transform.scale(self.sbishop_probe, (70,70))
			self.sbb_img = pygame.transform.rotozoom(self.sbn_img, 180, 1)

			self.kn_img = pygame.transform.scale(self.kingn_probe, (70,70))

			self.kb_img = pygame.transform.scale(self.kingb_probe, (70,70))
			self.kb_img = pygame.transform.rotozoom(self.kb_img, 180, 1)
		else:
			self.pb_img = pygame.transform.scale(self.pawn_probe, (70,70))
			self.pn_img = pygame.transform.rotozoom(self.pb_img, 180, 1)

			self.spb_img = pygame.transform.scale(self.spawn_probe, (70,70))
			self.spn_img = pygame.transform.rotozoom(self.spb_img, 180, 1)

			self.lb_img = pygame.transform.scale(self.lance_probe, (70,70))
			self.ln_img = pygame.transform.rotozoom(self.lb_img, 180, 1)

			self.slb_img = pygame.transform.scale(self.slance_probe, (70,70))
			self.sln_img = pygame.transform.rotozoom(self.slb_img, 180, 1)

			self.nb_img = pygame.transform.scale(self.knight_probe, (70,70))
			self.nn_img = pygame.transform.rotozoom(self.nb_img, 180, 1)

			self.snb_img = pygame.transform.scale(self.sknight_probe, (70,70))
			self.snn_img = pygame.transform.rotozoom(self.snb_img, 180, 1)

			self.sb_img = pygame.transform.scale(self.silver_probe, (70,70))
			self.sn_img = pygame.transform.rotozoom(self.sb_img, 180, 1)

			self.ssb_img = pygame.transform.scale(self.ssilver_probe, (70,70))
			self.ssn_img = pygame.transform.rotozoom(self.ssb_img, 180, 1)

			self.gb_img = pygame.transform.scale(self.gold_probe, (70,70))
			self.gn_img = pygame.transform.rotozoom(self.gb_img, 180, 1)

			self.tb_img = pygame.transform.scale(self.tower_probe, (70,70))
			self.tn_img = pygame.transform.rotozoom(self.tb_img, 180, 1)

			self.stb_img = pygame.transform.scale(self.stower_probe, (70,70))
			self.stn_img = pygame.transform.rotozoom(self.stb_img, 180, 1)

			self.bb_img = pygame.transform.scale(self.bishop_probe, (70,70))
			self.bn_img = pygame.transform.rotozoom(self.bb_img, 180, 1)

			self.sbb_img = pygame.transform.scale(self.sbishop_probe, (70,70))
			self.sbn_img = pygame.transform.rotozoom(self.sbb_img, 180, 1)

			self.kb_img = pygame.transform.scale(self.kingb_probe, (70,70))

			self.kn_img = pygame.transform.scale(self.kingn_probe, (70,70))
			self.kn_img = pygame.transform.rotozoom(self.kn_img, 180, 1)

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
		reg = re.compile('\[[^\[\]]*\]')
		self.metadata = reg.findall(self.raw)
		for e in self.metadata:
			self.raw = self.raw.replace(e, '')

	def get_names(self):
		sente = re.compile('\[([Ss]ente|[Bb]lack)[:\s][^\[\]]*"([a-zA-z0-9][^\[\]]*)"\s*\]')
		gote = re.compile('\[([Gg]ote|[Ww]hite)[:\s][^\[\]]*"([a-zA-z0-9][^\[\]]*)"\s*\]')
		for e in self.metadata:
			if sente.match(e):
				self.sente = sente.match(e).group(2)
			elif gote.match(e):
				self.gote = gote.match(e).group(2)
	
	def prepare_movs(self):
		reg = re.compile('(\+?[P|L|N|S|G|K|R|B](\d[a-i])?[-|x|*]\d[a-i][=|\+]?)')
		moves = reg.findall(self.raw)
		output = ''
		if moves == []:
			tkMessageBox.showerror("NO NOTATIONS FOUND", "This file doesn't contain correct shogi western notations.")
			exit()
		for i in xrange(0, len(moves)):
			if output != '':
				output += '\n'
			if str(type(moves[i])) == "<type 'tuple'>":	
				output += str(i+1) + ' - ' +moves[i][0]
			else:
				output += str(i+1) + ' - ' +moves[i]
		self.movs = output
