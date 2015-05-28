#!/usr/bin/env python
# * coding: utf-8 *

### WARNING: This script is outdated, it needs a very specific notation format to work.

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
This script reverts notations's coords to correct them,
for cases in which they have been recorded in the inverse order
"""


import re, Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()

partida = open(file_path,'r')
movs = partida.read().splitlines()
partida.close()

reg = re.compile('^(\s*\d+-\s)(.*)([-|x|\*])(.*)$')

coords_a = {
    '1': '9',
    '2': '8',
    '3': '7',
    '4': '6',
    '5': '5',
    '6': '4',
    '7': '3',
    '8': '2',
    '9': '1'
}
coords_b = {
    'i': 'a',
    'h': 'b',
    'g': 'c',
    'f': 'd',
    'e': 'e',
    'd': 'f',
    'c': 'g',
    'b': 'h',
    'a': 'i'
}

output = ''
for e in movs:
    piece_x = ''
    piece_y = ''
    extra = ''
    frag = reg.match(e)
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

    dest_x = coords_a[frag.group(4)[0]]
    dest_y = coords_b[frag.group(4)[1]]

    if len(frag.group(4)) == 3:
        extra = frag.group(4)[2]

    output += frag.group(1) + kind + piece_x + piece_y + frag.group(3) + dest_x + dest_y + extra + '\n'

#TODO This regexp should probably be more accurate than this
slash = re.match('^(.*)(\.\w*)$', file_path)

frag_path = slash.group(1)
ext = slash.group(2)

partida_inv = open(frag_path+'_mod'+ext,'w')
partida_inv.write(output)
partida_inv.close()
