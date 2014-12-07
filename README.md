shogi_reader
============

Script that uses pygame to convert Shogi Western Notation into easily-replayable games.

### ABOUT ShogiReader ###

This program goal is to read shogi games saved in plain text using Western Shogi Game Notation (see http://japanesechess.org/notation/shogi_notation.html for more details) and use that information to replay every move forwards and backwards. It is a prototype, but it works. You switch to the next move pressing D, and to the previous pressing A. Now you can also rotate the board 180º pressing R key. 

### SOME THINGS THAT NEED IMPROVEMENT ###

I will slowly improve some of these things and more when I have some spare time, but any commit made by other users to improve the program is appreciated.

*1* The notation reading algorythm is not flexible enough because it must be read strictly with this kind of structure -for instance like this:

	  1- G-7h
	  2- P-3d
	  3- P-7f
	  4- P-4d
	  5- P-2f
	  6- S-4b
	  7- S-6h

I use <a href="https://github.com/SebasSBM/shogi_reader/blob/master/shogi_reader.py#L111">this regexp</a> to gather the information to be processed:
<code>
	reg = re.compile('^\s*(\d+)\s*-\s*(\+?[P|L|N|S|G|K|R|B](\d[a-i])?)([-|x|*])(\d[a-i][=|\+]?)$')
</code>

  So, in objects returned by match() function (for instance, called "frag"), frag.group(1) would be the turn number -this is not mandatory for counting the turns through, or it should not be I should say-; frag.group(2) would be the kind of piece moved and desambiguation coords(if included); frag.group(3) gathers if it is a normal move("-"), a capture("x") or a piece drop("*");frag.group(4) would be the rest of the notation -coords where the piece is moved to and promoting symbols if they are present.

  It works perfectly to read the Western Notation, but the algorythm itself is not any flexible about how the different moves are listed. It would fail, for example, if the example above was listed like this:

		G-7h
		P-3d
		P-7f
		P-4d
		P-2f
		S-4b
		S-6h

or this:

	  1- G-7h  P-3d
	  2- P-7f  P-4d
	  3- P-2f  S-4b

...among other possible list structures. It would be good that the algorythm was more flexible with this, implementing several different regexps to gather the data instead of just one.

*2* The program doesn't handle potential exceptions that may occurr if the game notation was incorrect.

  The most interesting exception to handle: for example, top-right square is 1a, and bottom-left 9i. If coords were reverted (notation rules say that black player -the first to move- must be at the top side of the board at the beginning. Reverted would mean that the first to move is at the bottom side), the algorythm doesn't detect any legal move and gets stuck. In order to correct this kind of wrong notations, I've made the script reverter.py that takes a notated game file and reverts every single coord. It would be interesting to implement revert.py's algorythm as a first step to handle an exception where no legal move is found by the computer in a line that matched the regexp that gathers the data (compiled to the variable "reg").

