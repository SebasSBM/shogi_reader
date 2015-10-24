shogi_reader
============

shogi_reader.py is a script that uses pygame to convert Shogi Western Notation into easily-replayable games.

### ABOUT ShogiReader ###

This program goal is to read shogi games saved in plain text using Western Shogi Game Notation (see http://japanesechess.org/notation/shogi_notation.html for more details) and use that information to replay every move forwards and backwards. It is a prototype, but it works. You switch to the next move pressing D, and to the previous pressing A. Now you can also rotate the board 180º pressing R key.

### REQUIREMENTS ###
This software is made with Python and uses the Pygame library to work, so, your OS needs to have:

- Python installed (usually, Linux based OS have Python installed by default, but there may be exceptions).
- Pygame library installed.

Global variables have been implemented to grant that the software will find the sprites properly no matter where the Shogi Reader is executed from.

I've not made a deep research about how to make pygame games work in Windows OS, but I know it is possible. Late or soon, I will implement good installation tools to make this software easy to install in Windows, Linux and MacOS.

### IMPROVEMENTS ###

I have already improved some things that are worth to be mentioned:

*1*- <b>Now notation reading is much more flexible than before.</b>

  Before, the input file with the notations needed to be listed like this:

	  1- G-7h
	  2- P-3d
	  3- P-7f
	  4- P-4d
	  5- P-2f
	  6- S-4b
	  7- S-6h

  Now it is not necessary anymore. The only thing needed now for the program to be able to render the notation is that **it must be correct** (see http://japanesechess.org/notation/shogi_notation.html).

  In other words, no matter if the notation is messy (for instance like this):

	  G-7hP-3d P-7f moves 1,2,3 xD P-4d P-2f [Text inside brackets is
	   interpreted as metadata and ignored by the moves renderer. So, even
	   if it contains notations P-7f -> B-7g they will be ignored and won't
	   interfere] S-4b -> S-6h

  The current version is able to read and render this mess as well as if it was like the first example.

*2*- **Metadata processing methods have been implemented.**

  Now, all content inside brackets [] is interpreted and listed as metadata. All this metadata is filtered out of the moves rendering process.

  The following instances will be used to show the player's names on screen:

	  [Sente: "Name of black player"] -> OR -> [Black: "Name of black player"]
	  [Gote: "Name of white player"] -> OR -> [White: "Name of white player"]


### SOME THINGS THAT NEED IMPROVEMENT ###

I will slowly improve some of these things and more when I have some spare time, but any commit made by other users to improve the program would be appreciated.

*1*- <b>Shogi rules are not fully implemented.</b>
   The moves rendering functions look only for legal moves when moving pieces. However, it could skip a move if there wasn't any piece able to perform that, doing what I call a "double turn moving" because that turn is skipped. It also overlooks any limitation about dropping captured pieces, then conditionals to prevent "funny" piece drops should also be implemented. Other thing has been overlooked is the promotion rules (you could place the symbol '+' after a move and piece would be promotioned even if it can't yet). Conditionals to detect illegal checkmates- checkmating with a pawn drop.- should also be implemented.

*2*- <b>The program doesn't handle all the potential exceptions yet.</b>

  Basic exception handling has already been implemented, but there are some potential exceptions that are not handled yet. Some of the exceptions pending of being created and/or handled are:
  
- Making sure that the piece can perform the move without breaking any shogi rule- as explained at point 2.
- Reverted Notation automatic handling, as explained below.
- Some other potential exceptions that I haven't figured out yet.

  The most interesting exception to handle: for example, top-right square is 1a, and bottom-left 9i. If coords were reverted (notation rules say that black player -the first to move- must be at the top side of the board at the beginning. Reverted would mean that the first to move is at the bottom side. See http://japanesechess.org/notation/shogi_notation.html for more details.), the algorithm doesn't detect any legal move and gets stuck. In order to correct this kind of wrong notations, I've made the script reverter.py that takes a notated game file and reverts every single coord. It would be interesting to implement revert.py's algorithm as a first step to handle an exception where no legal move is found by the computer in a line that matched the regexp that gathers the data (compiled to the variable "reg").
  
*3*- <b>Metadata reading and processing.</b>

  Recently, I've noticed that some of the notated games that you can find over the internet (like games played at <a href="http://playok.com">playok.com</a> or professional games notated and uploaded to the internet, like the ones I found in http://www2.teu.ac.jp/gamelab/SHOGI/kifumain.html) use to include some metadata, like:
  
- Names of both players.
- Date when the game was played.
- Comments about the match and why did the players make the decision they made.
    
...among other stuff. Metadata handling has already been implemented, but only player names are used by the program yet. Finding a good way to implement comments display is a good point. Also, maybe I should implement date displaying. It would be also interesting to implement some way to load a photo for certain player names, but I still have to think about the best way to implement this.

*4*- <b>Preparing a good installation script for as many operative systems as possible.</b>

*5* **More visual improvements for the GUI**
