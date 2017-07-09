#-------------------------------------------------------------------#
#	FEN Parsing Coding Challenge									#
#	Instructions can be found at:									#
#		http://files.lib.byu.edu/webdev-hire/instructions/			#
#	Author: Shayla Draper											#
#	Started: July 7, 2017											#
#	Completed: July 8, 2017											#
#-------------------------------------------------------------------#

import sys
import requests
import json
from collections import OrderedDict

#--------These constants are only used for testing purposes---------#
STARTING_SETUP = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
ALTERED_SETUP1 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
ALTERED_SETUP2 = "8/4npk1/5p1p/1Q5P/1p4P1/4r3/7q/3K1R2 b - - 1 49"
ALTERED_SETUP3 = "5r1k/6pp/4Qpb1/p7/8/6PP/P4PK1/3q4 b - - 4 37"
ALTERED_SETUP4 = "8/8/2P5/4B3/1Q6/4K3/6P1/3k4 w - - 5 67"
ALTERED_SETUP5 = "r2q1rk1/pp2ppbp/2p2np1/6B1/3PP1b1/Q1P2N2/P4PPP/3RKB1R b K - 0 13"
STARTING_MOVE = "a2a3"
ALTERED_MOVE1 = "a7a5"
#-------------------------------------------------------------------#

#Column to index lookup
col_to_idx = {
	'a' : 1,
	'b' : 2,
	'c' : 3,
	'd' : 4,
	'e' : 5,
	'f' : 6,
	'g' : 7,
	'h' : 8
}

#-------------------------------------------------------------------#
# Prints the chessboard neatly along with title and used FEN string	#
# Variables: 														#
#	2D list - chessboard											#
#	string - title													#
#	string - fenString												#
# Return: Void														#
#-------------------------------------------------------------------#
def printBoard(chessboard, title, fenString):
	#Define Constant Strings to use
	EDGE = "  ---------------------------------"
	BOUNDRY = "\n  |-------------------------------|"
	LOW_LABEL = "    a   b   c   d   e   f   g   h"

	#Set Bool to toggle if we have passed the first runthrough
	passedFirst = False
	print("\n  -------  " + title + "  -------")
	print(EDGE)

	#Iterate throught the [[]] in order to print the chessboard
	for line in chessboard:

		#Only print the boundry line if not printing first line
		if passedFirst: 
			print(BOUNDRY)
		passedFirst = True

		for i in range(0, 8):
			print (line[i], end = " | ")
		print(line[8], end = " |")

	print("\n" + EDGE)
	print(LOW_LABEL)
	print("\nFEN string Used:", fenString + '\n\n')
#------------------------- End printBoard --------------------------#

#-------------------------------------------------------------------#
# Generates the orignal chessboard									#
# Sets all board-spaces to an empty space character					#
# Variables: None 													#
# Return: 2D list - chessboard										#
#-------------------------------------------------------------------#
def generateBoard():
	chessboard = []
	line = []

	for x in range(0, 9):
		line.append(" ")
	for x in range(0, 8):
		line[0] = 8 - x
		chessboard.append(list(line))

	return chessboard
#------------------------ End generateBoard ------------------------#

#-------------------------------------------------------------------#
# Generates the orignal chessboard									#
# Sets all board-spaces to an empty space character					#
# If there are not the correct number of units indicate in the FEN, #
#	an error message is printed and the program exits 				#
# Variables: 														#
#	string - fenString												#
#	2D list - chessboard											#
# Return: 2D list - chessboard										#
#-------------------------------------------------------------------#
def parseFEN(fenString, chessboard):
	#Split given FEN string, assign piece locations to rows
	splitFEN = fenString.split(" ")

	#Check for valid FEN
	if (len(splitFEN) != 6):
		print("\nERROR: Invalid FEN string\n")
		sys.exit()

	#Split first part of FEN to retrieve rows
	rows = splitFEN[0].split('/')

	#Check for valid amount of rows in FEN
	if len(rows) != 8:
		print("\nERROR: Invalid FEN\n")
		sys.exit()

	#Iterate through the FEN string, assign piece location
	curRow = 0
	for row in rows:
		curIndex = 1

		for char in row:
			#Check for non-numeric, assign board position
			if char.isdigit() == False:
				chessboard[curRow][curIndex] = char
				curIndex += 1
			#If numeric, update the current index accordingly
			else:
				curIndex += int(char)
		curRow += 1

	return chessboard, splitFEN
#-------------------------- End parseFEN ---------------------------#

#-------------------------------------------------------------------#
# Parse the give move												#
# Set all chars to their respective ints in order to be usable		#
# Variables: string - move 											#
# Return: list - move 												#
#-------------------------------------------------------------------#
def parseMove(move):
	move = [move[0], move[1], move[2], move[3]]
	move[0] = col_to_idx[move[0]]
	move[1] = 8 - int(move[1])
	move[2] = col_to_idx[move[2]]
	move[3] = 8 - int(move[3])
	return move
#-------------------------- End parseMove --------------------------#

#-------------------------------------------------------------------#
# Update the current board											#
# Move the desired piece to the requested location by removing the 	#
#	inital piece location (set to " ") and replacing current piece 	#
#	info of new location with the info of the moving piece 			#
# Variables: 														#
#	2D list - chessboard											#
#	string - move 													#
# Return: 2D list - chessboard										#
#-------------------------------------------------------------------#
def updateBoard(chessboard, move):
	move = parseMove(move)
	movingPiece = chessboard[move[1]] [move[0]]
	chessboard[move[1]][move[0]] = " "
	chessboard[move[3]][move[2]] = movingPiece
	return chessboard
#------------------------- End updateBoard -------------------------#

#-------------------------------------------------------------------#
# Update the current FEN string										#
# Read the chessboard line by line add to a space count if the 		#
#	current index contains a space add the number of spaces once the#
#	end of a row or a character is reached. Add character if exists	#
# Variables: 														#
#	2D list - chessboard											#
#	list - splitFEN													#
# Return: string - newFEN 											#
#-------------------------------------------------------------------#
def updateFEN(chessboard, splitFEN):

	#Set Bool to toggle if we have passed the first runthrough
	passedFirst = False
	newFEN = ""

	#Iterate through the chessboard
	for row in chessboard:

		# Add '/' if beyond row marker number
		if passedFirst:
			newFEN += '/'
		passedFirst = True
		spaceCount = 0

		#For each piece, either pass, add spaceCount, or add newFEN 
		for piece in row:
			if piece == row[0]:
				pass
			elif piece == " ":
				spaceCount += 1
			else:
				if spaceCount > 0:
					newFEN += str(spaceCount)
				newFEN += piece
				spaceCount = 0

		if spaceCount > 0:
			newFEN += str(spaceCount)

	#Add the other FEN information to the updated FEN string
	for i in range(1, len(splitFEN)):
		newFEN += " " + splitFEN[i]
		
	return newFEN
#-------------------------- End updateFEN --------------------------#

#-------------------------------------------------------------------#
# Retrieve the next move from the API, ensure ordered dictionry to 	#
#	retrieve corret move, extract move 								#
# If there is an error in retrieving the move from the API, an error#
#	message is printed and the program exits 						#
# Variables: string - startingFEN									#
# Return: string - move 											#
#-------------------------------------------------------------------#
def getMove(startingFEN):
	try:
		getRequest = "https://syzygy-tables.info/api/v2?fen="
		results = requests.get(getRequest + startingFEN)
		data = json.loads(results.text, object_pairs_hook = OrderedDict)
		move = list(data['moves'].items())[0][0]
		print("Move Used:", move)
	except:
		print("ERROR: Unable to retrieve suggested move\n")
		sys.exit()
	return move
#--------------------------- End getMove ---------------------------#

#-------------------------------------------------------------------#
# Read in first line of the file given -- assume FEN string 		#
# Variables: string - fileName										#
# Return: string - fenString										#
#-------------------------------------------------------------------#
def readFile(fileName):
	with open(fileName) as file:
		fenString = file.readline().strip()
	return fenString
#-------------------------- End readFile ---------------------------#

#-------------------------------------------------------------------#
# Read in all the arguments after the program string and append to  #
#	the FEN string.  Assuming all remaining arguments are FEN string#
# Variables: 														#
#	list - sysArgs													#
#	int - sysArgLen													#
# Return: string - fenString										#
#-------------------------------------------------------------------#
def readArgs(sysArgs, sysArgLen):
	fenString = ""
	for i in range(1, sysArgLen):
		fenString += sysArgs[i] + " "

	#Remove last appended space
	fenString = fenString[:-1]
	return fenString
#-------------------------- End readArgs ---------------------------#

#-------------------------------------------------------------------#
# Generate board and initiate both parsing and updating.  Call board#
#	print functions													#
# Variables: string - fileName										#
#-------------------------------------------------------------------#
def main(sysArgs, sysArgLen):
	#Task One - Read and Parse FEN string
	chessboard = generateBoard()
	#Single argument indicates file, more indicates system call
	if (sysArgLen == 2):
		startingFEN = readFile(sysArgs[1])
	elif (sysArgLen == 7):
		startingFEN = readArgs(sysArgs, sysArgLen)
	else:
		print("\nERROR: Need FEN string or file containing FEN string\n")
		sys.exit()

	chessboard, splitFEN = parseFEN(startingFEN, chessboard)
	printBoard(chessboard, "Starting Board", startingFEN)

	#Task Two - Update FEN
	move = getMove(startingFEN)
	chessboard = updateBoard(chessboard, move)
	newFEN = updateFEN(chessboard, splitFEN)
	printBoard(chessboard, "Updated Board", newFEN)
#----------------------------- End main -----------------------------#

if __name__ == "__main__":
	main(sys.argv, len(sys.argv))
	
