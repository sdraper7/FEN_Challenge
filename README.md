# FEN_Challenge
FEN Parsing Challenge - BYU
Author: Shayla Draper
Full specifications can be found at: http://files.lib.byu.edu/webdev-hire/instructions/


Included in this zip repository are the following items:
	1.	fenChallenge.py - This document contains all of my source code.  It is written completely in Python
	2.	fenChallengeNotes.txt - These are the notes I took while I was creating this code
	3.	fenStr.txt (1-6) - These are text files that contain a starting FEN string each
	4.	This README document

To Run:
	If the FEN string is given through a text file, run the following command:
		python3 fenChallenge.py <text file containing FEN string>
		example: python3 fenChallenge.py fenStr1.txt
	If the FEN string is given via the command line, run the following command:
		python3 fenChallenge.py <Valid FEN string>
		example: python3 fenChallenge.py rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 1

Output:
	Given a FEN string in a file, the output of the code will contain the following:
		1. The initial setup of the board with the FEN string provided
		2. The move used to update the board
		3. The updated board and FEN string
