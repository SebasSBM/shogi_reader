shogi_reader
============

Script that uses pygame to convert Shogi Western Notation into easily-replayable games.

### ABOUT ShogiReader ###

This program goal is to read shogi games saved in plain text using Western Shogi Game Notation (see http://japanesechess.org/notation/shogi_notation.html for more details) and use that information to replay every move forwards and backwards. It is a prototype, but it works. You switch to the next move pressing D, and to the previous pressing A. Now you can also rotate the board 180º pressing R key.

### REQUIREMENTS ###
This software is made with Python and uses the Pygame library to work, so, your OS needs to have:

- Python installed (usually, Linux based OS have Python installed by default, but there may be exceptions).
- Pygame library installed.

For now, the main script(shogi_reader.py) must be run from the directory that contains it, or else the sprites won't be found by the script and the script won't work at all. I will prepare some global variables to wipe out this error ASAP.

I've not made a deep research about how to make pygame games work in Windows OS, but I know it is possible. Late or soon, I will implement good installation tools to make this software easy to install in Windows, Linux and MacOS.

### SOME THINGS THAT NEED IMPROVEMENT ###

I will slowly improve some of these things and more when I have some spare time, but any commit made by other users to improve the program would be appreciated.

*1*- <b>The notation reading algorythm is not flexible enough because it must be read strictly with this kind of structure -for instance like this:</b>

	  1- G-7h
	  2- P-3d
	  3- P-7f
	  4- P-4d
	  5- P-2f
	  6- S-4b
	  7- S-6h

I use <a href="https://github.com/SebasSBM/shogi_reader/blob/master/shogi_reader.py?ts=4#L111">this regexp</a> to gather the information to be processed: <pre><code>    reg = re.compile('^\s\*(\d+)\s\*-\s\*(\+?\[P|L|N|S|G|K|R|B\](\d[a-i])?)([-|x|\*])(\d[a-i][=|\\+]?)$')</code></pre>

  So, in objects returned by match() function (for instance, called "frag"), frag.group(1) would be the turn number -this is not mandatory for counting the turns though, or it should not be I should say-; frag.group(2) would be the kind of piece moved and desambiguation coords(if included); frag.group(3) gathers if it is a normal move("-"), a capture("x") or a piece drop("*");frag.group(4) would be the rest of the notation -coords where the piece is moved to and promoting symbols if they are present.

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

*2*- <b>Shogi rules are not fully implemented.</b>
  The algorythm that processes every move looks for the movement that every kind of piece has, but it overlooks the pieces that are in the way to the target coords. So, new conditionals must be implemented to check if there are pieces in the middle that are blocking the way. And, if they are, and no other piece can make the move, an exception should be thrown telling that the notation is incorrect. In addition, it also overlooks any limitation about dropping captured pieces, then conditionals to prevent "funny" piece drops should also be implemented. And I also should implement conditionals to detect illegal checkmates- checkmating with a pawn drop. As I explain in the 3rd point, I haven't begun to prepare exception handling yet.

*3*- <b>The program doesn't handle potential exceptions that may occurr if the game notation was incorrect nor other stuff.</b>

  I haven't begun with exception handling routines yet, because my main priority until now was just to make this work with correct notations and to implement the basic features -captured pieces sprites, last move highlighting and the feature to reverse the board at any moment-. Now that this basic features are ready, my next task will probably be to start implementing basic exception handling. Some of the exceptions that should be created and/or handled are:
  
- Making sure that the piece can perform the move without breaking any shogi rule- as explained at point 2.
- Exceptions for when the regexp that splits the data of a line to be processed just doesn't match.
- Exceptions when no legal move is detected for that line.
- Exceptions when the notation of a single move allows more than one piece to perform the move (ambiguity warning).
- Exception when you click "Cancel" in the loading game dialog box (Python throws "No such file" in this situation, but it would be cool to prepare a more clean way to handle this exception).

  The most interesting exception to handle: for example, top-right square is 1a, and bottom-left 9i. If coords were reverted (notation rules say that black player -the first to move- must be at the top side of the board at the beginning. Reverted would mean that the first to move is at the bottom side), the algorythm doesn't detect any legal move and gets stuck. In order to correct this kind of wrong notations, I've made the script reverter.py that takes a notated game file and reverts every single coord. It would be interesting to implement revert.py's algorythm as a first step to handle an exception where no legal move is found by the computer in a line that matched the regexp that gathers the data (compiled to the variable "reg").
  
*4*- <b>Metadata reading and processing.</b>

  Recently, I've noticed that some of the notated games that you can find over the internet (like games played at playok.com or professional games notated and uploaded to the internet) use to include some metadata, like:
  
- Names of both players.
- Date when the game was played.
- Comments about the match and why did the players make the decision they made.
    
...among other stuff. It would be interesting to implement player's name gathering and comments in the first place, and, maybe, other stuff too.

*5*- <b>Preparing a good installation script for as many operative systems as possible.</b>
