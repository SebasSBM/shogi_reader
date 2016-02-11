#!/usr/bin/env python
# * coding: utf-8 *

from managers import CoordsManager, InputManager, MatrixManager

# *** Global variables ***
history = []
pos = 0
lamesa = CoordsManager()

import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename(filetypes = (('*.TXT files','*.txt'),('ALL FILES','*')))
if file_path == '':
    exit()
partida = open(file_path, 'r')

rawgame = partida.read()
game_data = InputManager(rawgame)

matrix = MatrixManager()
