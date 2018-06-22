import pygame
import sys
from time import time
from pygame.locals import*
import copy
from random import randint

white = (255, 255, 255)         #color for white squares
grey = (0,0,0)                  #color for black squares
red = (255, 80, 80)             #color for computer pieces
blue = (0, 153, 255)            #color for human pieces
highlightedColor = (255,255,153)    #color if the square is selected
topRight = "topright"           #directions used in different functions within the source code
topLeft = "topleft"
bottomRight = "bottomright"
bottomLeft = "bottomleft"
MaxPrunes = 0
MinPrunes = 0
TotalNumberOfNodes = 1


'''Squares class is used to store different checkerPieces. The whole board is made up of these squares
initialized with 2 attrivutes that is color and whether it is occupied or not if occupied , then occupied by which checkerpiece'''

class squares:
    def __init__(self, color = None,occupied = None):
        self.color = color
        self.occupied = occupied


'''Checkerpiece class is created to store the checkerpieces. It has single attribute which is color to determine whether the piece is
for human or computer'''

class checkerPeice:
    def __init__(self, color):
        self.color = color


'''Board class is created to store the board matrix. All the functions regarding the movement of pieces within the board are mentioned in the Board class'''

class Board:
    def __init__(self):
        self.boardmatrix = self.initialBoard()
        self.boardmatrix2 = self.initialBoard()

    def copy1(self):
        return copy.deepcopy(self)      #this is used to copy the object into another copy. Deepcopy copies the object rather than the reference

    def initialBoard(self):             #function defined to initialize the board- returns the 2Darray of the board
        boardmatrix = [[None for x in range(6)] for y in range(6)]
        #initial board- each position of the 2D array is being initialized as an object of the Squares class
        for x in range(6):
            for y in range(6):
                if (x%2 == 0) and (y%2 ==0):
                    boardmatrix[x][y] = squares(white)
                elif (x%2 == 0) and (y%2 !=0):
                    boardmatrix[x][y] = squares(grey)
                elif (x%2 != 0) and (y%2 ==0):
                    boardmatrix[x][y] = squares(grey)
                elif (x%2 != 0) and (y%2 !=0):
                    boardmatrix[x][y] = squares(white)

        #initial pieces - initial pieces are placed within the initial squares of the board
        for x in range(6):
            for y in range(2):
                if boardmatrix[x][y].color == grey:
                    boardmatrix[x][y].occupied = checkerPeice(red)
            for y in range(4, 6):
                if boardmatrix[x][y].color == grey:
                    boardmatrix[x][y].occupied = checkerPeice(blue)

        return boardmatrix

    def movement(self, direction, (x, y)):

        # the coordinates which will be after the movement of the checker pieces
        if direction == topRight:
            return (x+1, y-1)
        elif direction == topLeft:
            return (x-1, y-1)
        elif direction == bottomLeft:
            return (x-1, y+1)
        elif direction ==bottomRight:
            return (x+1, y+1)
        else:
            return (-1,-1)

    def new_board(self,boardmatrix):            # this function is used to return a matrix which has the colors of the squares in the board
        newBoard = [[None] for y in range(6)]

        for i in range(6):
            for j in range(6):
                if boardmatrix[i][j].color == white:
                    newBoard[i][j] = "white"
                else:
                    newBoard[i][j] = "grey"

        return newBoard

    def diagonalSquareLocation(self,(x,y)):         #function used to an array of all the adjacent positions
        return [self.movement(topLeft,(x,y)), self.movement(topRight,(x,y)),self.movement(bottomLeft,(x,y)),self.movement(bottomRight,(x,y))]

    def currentLocation(self,(x,y)):            #function takes in a tuple of the current coordinates and return the reference to the position on the board
        return self.boardmatrix[x][y]


    def movesWithoutLooking(self, (x,y)):       #function used to obtain the blind moves that can be taken by a piece at position (x,y)
        movesWithoutLooking = []                #initialize an empty array to store the blind moves
        if self.boardmatrix[x][y].occupied != None:     #check if any checkerpiece present at (x,y)
            if self.boardmatrix[x][y].occupied.color == blue:       #check which piece is present. Blue is for human
                movesWithoutLooking = [self.movement(topLeft,(x,y)),self.movement(topRight,(x,y))]      #two blind moves are appended to the array for blind moves
            elif self.boardmatrix[x][y].occupied.color == red:  #check which piece is present. Red piece for computer
                movesWithoutLooking = [self.movement(bottomLeft,(x,y)),self.movement(bottomRight,(x,y))]        #two blind moves for PC appended
            else:
                movesWithoutLooking = []
        return movesWithoutLooking

    def legalMoves(self,(x,y)):     #function is used to return an array of legal moves by eliminating the moves not possible in blind moves
        movesWithoutLooking = self.movesWithoutLooking((x,y))       #store the blind moves of position (x,y) in an array
        legalMoves = []     #initialize an empty array for legal moves

        for moves in movesWithoutLooking:           #move is a tuple in the form of (x,y) which shows the coordinate where the piece can go from current position
            if self.checkValidLocation(moves):          #check whether the move is present on the board or not
                if self.currentLocation(moves).occupied == None:
                    legalMoves.append(moves)        #if the position which was being checked is empty, the checkerpiece from (x,y) can be shifted to this move
                elif self.currentLocation(moves).occupied.color != self.currentLocation((x,y)).occupied.color and self.checkValidLocation((moves[0]+(moves[0]-x),moves[1] + (moves[1]-y))) and self.currentLocation((moves[0]+(moves[0]-x),moves[1] + (moves[1]-y))).occupied == None:
                    legalMoves.append((moves[0]+(moves[0]-x),moves[1]+(moves[1]-y)))       #if the move is filled by an enemy piece, check if a capture move is possible or not.If capture is possible, append the new move position to the legal moves array.

        return legalMoves   #an array of legal moves which also includes the capture moves


    def movesWithoutLooking3(self):     # another function for blind moves is created as it takes in only the object as a parameter and does not need the coordinates.
                                        #This function is needed to record the blind moves for the whole board state
        movesWithoutLooking3 = []   # the tuple is of the form((xStartPos,yStartPos,xCoordinteMove,yCoordinateMove)
        # print self.boardmatrix
        for x in range(6):
            for y in range(6):
                # print self.boardmatrix[x][y],"board matrix"
                if self.boardmatrix[x][y].occupied != None:        #check if the position is empty or not
                    if self.boardmatrix[x][y].occupied.color == red:        #if position occupied by red checkerpiece
                        firsttMoveWithoutLooking = (self.movement(bottomLeft, (x, y)))
                        secondmoveWithoutLooking = (self.movement(bottomRight, (x, y)))
                        movesWithoutLooking3.append((x,y,firsttMoveWithoutLooking[0],firsttMoveWithoutLooking[1]))      #first blind move appended as a tuple with the start coordinates first and then the final coordinates
                        movesWithoutLooking3.append((x,y,secondmoveWithoutLooking[0],secondmoveWithoutLooking[1]))      #second blind move appended as a tuple with the start coordinates first and then the final coordinates
                    elif self.boardmatrix[x][y].occupied.color != blue:     #if position empty
                        movesWithoutLooking3.append((-1, -1,-1,-1))
        return movesWithoutLooking3     #array of tuples of blind moves returned

    def legalMoves3(self):  #function to obtain the legal moves of the computer from it's blind moves
        legalMoves3 = []    #initialize an array to store the legal moves
        movesWithoutLooking3 = self.movesWithoutLooking3()   #store the blind moves into a new array
        for moves in movesWithoutLooking3:      #moves is in the form of a tuple as (startingx,startingy,finalx,finaly)
            if self.checkValidLocation((moves[2],moves[3])):   #check if the final position of the move is valid location or not
                if self.currentLocation((moves[2],moves[3])).occupied == None:  #if the final position is empty append the move as a legal move
                    legalMoves3.append(moves)
                elif self.currentLocation((moves[2],moves[3])).occupied.color == blue and self.checkValidLocation((moves[2] + (moves[2] - moves[0]), moves[3] + (moves[3] - moves[1]))) and self.currentLocation((moves[2] + (moves[2] - moves[0]), moves[3] + (moves[3] - moves[1]))).occupied == None:
                    legalMoves3.append((moves[0],moves[1],moves[2]+(moves[2]-moves[0]),moves[3]+(moves[3]-moves[1])))   #if the final position is occupied by the enemy piece, check if it can be treated as a capture move. If a capture is possible
                                                                                                                        #append the capture move in the array
        return legalMoves3  #an array of tuples of legal moves for computer

    def movesWithoutLooking3forMin(self):       #another blind function created to record the blind moves for the human player
        movesWithoutLooking3forMin = []   # the tuple is of the form((xStartPos,yStartPos,xCoordMove,yCoordMove)
        for x in range(6):
            for y in range(6):
                if self.boardmatrix[x][y].occupied != None:     #check if the position is empty or not
                    if self.boardmatrix[x][y].occupied.color == blue:       #check if the position occupied by human player
                        firsttMoveWithoutLooking = (self.movement(topLeft, (x, y)))
                        secondmoveWithoutLooking = (self.movement(topRight, (x, y)))
                        movesWithoutLooking3forMin.append((x,y,firsttMoveWithoutLooking[0],firsttMoveWithoutLooking[1])) #first blind move appended as a tuple with the start coordinates first and then the final coordinates
                        movesWithoutLooking3forMin.append((x,y,secondmoveWithoutLooking[0],secondmoveWithoutLooking[1]))#second blind move appended as a tuple with the start coordinates first and then the final coordinates
                    elif self.boardmatrix[x][y].occupied.color != blue:     #if position empty
                        movesWithoutLooking3forMin.append((-1, -1,-1,-1))
        return movesWithoutLooking3forMin   #array of blind moves for the human player

    def legalMoves3forMin(self):        #function to obtain the legal moves out of the blind moves of computer when only the object is the parameter
        legalMoves3forMin = []          #initialize an empty array to store the legal moves
        movesWithoutLooking3forMin = self.movesWithoutLooking3forMin()      #blind moves stored in new array
        for moves in movesWithoutLooking3forMin:        #moves is in the form of a tuple of (startingx,startingy,finalx,finaly)
            if self.checkValidLocation((moves[2],moves[3])):        #check if the final position of the checker piece is valid location or not
                if self.currentLocation((moves[2],moves[3])).occupied == None:   #if the final position of the checker piece move is empty append it to the legal moves array
                    legalMoves3forMin.append(moves)
                elif self.currentLocation((moves[2],moves[3])).occupied.color == red and self.checkValidLocation((moves[2] + (moves[2] - moves[0]), moves[3] + (moves[3] - moves[1]))) and self.currentLocation((moves[2] + (moves[2] - moves[0]), moves[3] + (moves[3] - moves[1]))).occupied == None:
                    legalMoves3forMin.append((moves[0],moves[1],moves[2]+(moves[2]-moves[0]),moves[3]+(moves[3]-moves[1])))   #if the final position has an enemy piece, check for a capture move and append if a capture move is found
        return legalMoves3forMin        #array of tuplpes of legal moves



    def checkValidLocation(self, coordinates):  #function to check if the coordinates are present on the board or outside the board index
        if coordinates[0] < 0 or coordinates[0] > 5 or coordinates[1] < 0 or coordinates[1] > 5:
            return False
        else:
            return True

    def pieceRemoval(self,(x,y)):   #removes the piece from the position(x,y)
        self.boardmatrix[x][y].occupied = None

    def movementPiece1(self,(initialx,initialy),(finalx,finaly)):   #moves the piece from (initialx, initialy) to (finalx, finaly)
        self.boardmatrix[finalx][finaly].occupied = self.boardmatrix[initialx][initialy].occupied
        self.pieceRemoval((initialx,initialy))

    def movementPiece(self,(initialx,initialy),(finalx,finaly)):    #moves the piece from (initialx, initialy) to (finalx, finaly). Also removes the enemy piece if the movement is of a capture move
        if (finaly-initialy) ==2:       # indicates a capture move
            self.boardmatrix[finalx][finaly].occupied = self.boardmatrix[initialx][initialy].occupied
            self.pieceRemoval((initialx,initialy))
            self.pieceRemoval(((int)((initialx+finalx)/2),(int)((initialy+finaly)/2)))
        else:   #indicates a normal movement
            self.boardmatrix[finalx][finaly].occupied = self.boardmatrix[initialx][initialy].occupied
            self.pieceRemoval((initialx,initialy))

    def movementPieceReturnsArray(self, (initialx, initialy), (finalx, finaly)):    #does the same task as movementPiece function but returns an array unlike the original function
        if (finaly - initialy) == 2 or (initialy - finaly) == 2:    #a capture move
            self.boardmatrix[finalx][finaly].occupied = self.boardmatrix[initialx][initialy].occupied
            self.pieceRemoval((initialx, initialy))
            self.pieceRemoval(((int)((initialx + finalx) / 2), (int)((initialy + finaly) / 2)))
        else:   #normal movement
            self.boardmatrix[finalx][finaly].occupied = self.boardmatrix[initialx][initialy].occupied
            self.pieceRemoval((initialx, initialy))
        return self.boardmatrix

    def checkForEndOfBoard(self,position):  #to see if the piece reaches the final row of the board for both computer and human. Position is a tuple of (x,y)
        if position[1] == 0 or position[1] == 5: #0th row is last row for human and 5th row is last for computer
            return True
        else:
            return False

    def terminalTest(self): # to check if the object is at the terminal state or not
        legalMoves3 = self.legalMoves3()    #legalMoves for the computer currently
        legalMoves3forMin = self.legalMoves3forMin()    #legal moves for the human currently
        terminalTest = False
        for i in range(6):
            for j in range(6):
                if legalMoves3 == [] and legalMoves3forMin ==[]:    #if the legal moves available for both human and computer is null, then a terminal stage has been reached
                    terminalTest = True
                else:
                    terminalTest = False
                    break
            if terminalTest == True:
                continue
            else:
                break
        return terminalTest     #returns True if terminal stage reached , else False

    def valueCalculation2(self):
        redScore = 0
        blueScore = 0
        for i in range(6):
            for j in range(6):
                if self.boardmatrix[i][j].occupied !=None and  self.boardmatrix[i][j].occupied.color == red:
                    if j ==0:
                        redScore = redScore+0
                    elif j ==1:
                        redScore = redScore+0
                    elif j ==2:
                        redScore = redScore+10
                    elif j ==3:
                        redScore = redScore+10
                    elif j ==4:
                        redScore = redScore+30
                    elif j== 5:
                        redScore = redScore+30
                elif self.boardmatrix[i][j].occupied !=None and  self.boardmatrix[i][j].occupied.color == blue:
                    if j ==5:
                        blueScore = blueScore-0
                    elif j ==4:
                        blueScore = blueScore-0
                    elif j ==3:
                        blueScore = blueScore-10
                    elif j ==2:
                        blueScore = blueScore -10
                    elif j ==1:
                        blueScore = blueScore-30
                    elif j ==0:
                        blueScore = blueScore-30
        score = redScore+blueScore
        print score , "score"
        return score

    def valueCalculation3(self):        # function to calculate the value of the states
        redScore = 0        #score for computer
        blueScore = 0       #score for human
        for j in range(1,6):
            if self.boardmatrix[1][0].occupied != None and self.boardmatrix[1][0].color == red: #if computer piece  in the first row
                redScore = redScore+1  #5 #10
            if self.boardmatrix[3][0].occupied != None and self.boardmatrix[3][0].color == red: #if computer piece  in the first row
                redScore = redScore+1  #5 #10
            if self.boardmatrix[5][0].occupied != None and self.boardmatrix[5][0].color == red:#if computer piece  in the first row
                redScore = redScore+1  #5 #10
            if  self.boardmatrix[j][1].occupied != None and self.boardmatrix[j][1].color == red:#if computer piece  in the second row
                redScore = redScore +2  #3 #8
            if self.boardmatrix[j][2].occupied != None and self.boardmatrix[j][2].color == red:#if computer piece  in the third row
                redScore = redScore + 2 #3 #7
            if self.boardmatrix[j][3].occupied != None and self.boardmatrix[j][3].color == red:#if computer piece  in the fourth row
                redScore = redScore + 3 #2 #6
            if self.boardmatrix[j][4].occupied != None and self.boardmatrix[j][4].color == red:#if computer piece  in the fifth row
                redScore = redScore + 5 #1 #4
            if self.boardmatrix[j][5].occupied != None and self.boardmatrix[j][5].color == red:#if computer piece  in the sixth row
                redScore = redScore + 5 #1 #4
        for j in range(5):
            if self.boardmatrix[1][5].occupied != None and self.boardmatrix[1][5].color == blue:#if human piece in the first row for human
                blueScore = blueScore - 1  #5 #10
            if self.boardmatrix[3][5].occupied != None and self.boardmatrix[3][5].color == blue:#if human piece in the first row for human
                blueScore = blueScore - 1  #5 #10
            if self.boardmatrix[5][5].occupied != None and self.boardmatrix[5][5].color == blue:#if human piece in the first row for human
                blueScore = blueScore - 1  #5 #10
            if self.boardmatrix[j][0].occupied != None and self.boardmatrix[j][0].color == blue:#if human piece in the second row for human
                blueScore = blueScore -5    #1 #4
            if self.boardmatrix[j][1].occupied != None and self.boardmatrix[j][1].color == blue:#if human piece in the third row for human
                blueScore = blueScore -5    #1 #4
            if self.boardmatrix[j][2].occupied != None and self.boardmatrix[j][2].color == blue:#if human piece in the fourth row for human
                blueScore = blueScore - 3   #2 #6
            if self.boardmatrix[j][3].occupied != None and self.boardmatrix[j][3].color == blue:#if human piece in the fifth row for human
                blueScore = blueScore -2    #3 #7
            if self.boardmatrix[j][4].occupied != None and self.boardmatrix[j][4].color == blue:#if human piece in the sixth row for human
                blueScore = blueScore -2    #3 #8
        for i in range(6):
            for j in range(6):
                if self.boardmatrix[i][j].occupied !=None and self.boardmatrix[i][j].occupied.color == red : #if current position is computer piece
                    if self.isCapturePositionRed(self.boardmatrix,(i,j)): #Can the computer piece perform a capture?
                        redScore = redScore+10  #award points if it can
                    else:
                        redScore = redScore+0   #no points if it cant
                    if self.isSafePositionForRed(self.boardmatrix,(i,j)):   #Is the piece itself safe from any Capture?
                        redScore = redScore+13  #award points if it is safe
                    else:
                        redScore = redScore-13  #deduct points if unsafe
                    redScore = redScore + (int)((5-j)/2.7)  #add points on the basis of distance from the last row of all pieces
                elif self.boardmatrix[i][j].occupied != None and self.boardmatrix[i][j].occupied.color == blue: #if current position is human piece
                    if self.isCapturePositionBlue(self.boardmatrix,(i,j)): #Can the human piece perform a capture?
                        blueScore = blueScore-13 #award points if it can
                    else:
                        blueScore = blueScore-0 #no points if it cant
                    if self.isSafePositionForBlue(self.boardmatrix,(i,j)): #Is the piece itself safe from any Capture?
                        blueScore = blueScore-13  #award points if it is safe
                    else:
                        blueScore = blueScore+13  #deduct points if unsafe
                    blueScore = blueScore - (int)(j/2.7)  #add points on the basis of distance from the last row of all pieces
        for j in range(6):  #check if the pieces are on the left and right walls of the board
            if self.boardmatrix[0][j].occupied !=None and self.boardmatrix[0][j].occupied.color == red:
                redScore = redScore+3
            elif self.boardmatrix[0][j].occupied !=None and self.boardmatrix[0][j].occupied.color == blue:
                blueScore = blueScore-3
            if self.boardmatrix[5][j].occupied != None and self.boardmatrix[5][j].occupied.color == red:
                redScore = redScore + 3
            elif self.boardmatrix[5][j].occupied != None and self.boardmatrix[5][j].occupied.color == blue:
                blueScore = blueScore - 3

        score = redScore+blueScore      #add the computer score and human score to get the final score
        return score

    def isSafePositionForRed(self,state,position):      #function to check if current position safe for computer piece.Takes input the current 2D matrix of board and tuple of current position
        newObject3 = Board()        #new object created so that original object's values are unchanged
        newObject3.boardmatrix = copy.deepcopy(state)   #deepcopy performed to copy the object rather than the reference
        blindmove1 = newObject3.movement(bottomRight,(position[0],position[1]))     #blindmoves created
        blindmove2 = newObject3.movement(bottomLeft,(position[0],position[1]))
        isSafe = True
        if newObject3.checkValidLocation(blindmove1):
            if newObject3.currentLocation(blindmove1).occupied != None and newObject3.currentLocation(blindmove1).occupied.color==blue:
                if newObject3.checkValidLocation((position[0]+(position[0]-blindmove1[0]),position[1]+(position[1]-blindmove1[1]))):
                    if newObject3.currentLocation((position[0]+(position[0]-blindmove1[0]),position[1]+(position[1]-blindmove1[1]))).occupied ==None:
                        isSafe = False  #if capture is possible by enemy piece return False
        if newObject3.checkValidLocation(blindmove2):
            if newObject3.currentLocation(blindmove2).occupied != None and newObject3.currentLocation(blindmove2).occupied.color!=blue:
                if newObject3.checkValidLocation((position[0]+(position[0]-blindmove2[0]),position[1]+(position[1]-blindmove2[1]))):
                    if newObject3.currentLocation((position[0]+(position[0]-blindmove2[0]),position[1]+(position[1]-blindmove2[1]))).occupied ==None:
                        isSafe = False  #if capture is possible by enemy piece return False
        return isSafe

    def isSafePositionForBlue(self, state, position): #function to check if current position safe for human piece.Takes input the current 2D matrix of board and tuple of current position
        newObject3 = Board()    #new object created so that original object's values are unchanged
        newObject3.boardmatrix = copy.deepcopy(state)   #deepcopy performed to copy the object rather than the reference
        blindmove1 = newObject3.movement(topRight, (position[0], position[1]))
        blindmove2 = newObject3.movement(topLeft, (position[0], position[1]))       #blindmoves created
        isSafe = True
        if newObject3.checkValidLocation(blindmove1):
            if newObject3.currentLocation(blindmove1).occupied != None and newObject3.currentLocation(blindmove1).occupied.color == red:
                if newObject3.checkValidLocation((position[0] + (position[0] - blindmove1[0]), position[1] + (position[1] - blindmove1[1]))):
                    if newObject3.currentLocation((position[0] + (position[0] - blindmove1[0]),position[1] + (position[1] - blindmove1[1]))).occupied == None:
                        isSafe = False  #if capture is possible by enemy piece return False
        if newObject3.checkValidLocation(blindmove2):
            if newObject3.currentLocation(blindmove2).occupied != None and newObject3.currentLocation(blindmove2).occupied.color != red:
                if newObject3.checkValidLocation((position[0] + (position[0] - blindmove2[0]), position[1] + (position[1] - blindmove2[1]))):
                    if newObject3.currentLocation((position[0] + (position[0] - blindmove2[0]),position[1] + (position[1] - blindmove2[1]))).occupied == None:
                        isSafe = False  #if capture is possible by enemy piece return False
        return isSafe

    def isCapturePositionRed(self,state,position):  #Can the piece at position tuple perform a capture move?
        newObject2 = Board()    #new object created so that original object's values are unchanged
        newObject2.boardmatrix = copy.deepcopy(state)   #deepcopy performed to copy the object rather than the reference
        blindmove1 = newObject2.movement(bottomRight,(position[0],position[1]))
        blindmove2 = newObject2.movement(bottomLeft,(position[0],position[1]))      #blindmoves created
        captureAnswer = False
        if newObject2.checkValidLocation(blindmove1):
            if newObject2.currentLocation(blindmove1).occupied!=None and newObject2.currentLocation(blindmove1).occupied.color!=newObject2.currentLocation(position).occupied.color :
                if newObject2.checkValidLocation((blindmove1[0]+(blindmove1[0]-position[0]),blindmove1[1]+(blindmove1[1]-position[1]))):
                    if newObject2.currentLocation((blindmove1[0]+(blindmove1[0]-position[0]),blindmove1[1]+(blindmove1[1]-position[1]))).occupied == None:
                        captureAnswer= True #capture move possible
        if newObject2.checkValidLocation(blindmove2):
            if newObject2.currentLocation(blindmove2).occupied!=None and newObject2.currentLocation(blindmove2).occupied.color!=newObject2.currentLocation(position).occupied.color :
                if newObject2.checkValidLocation((blindmove2[0]+(blindmove2[0]-position[0]),blindmove2[1]+(blindmove2[1]-position[1]))):
                    if newObject2.currentLocation((blindmove2[0]+(blindmove2[0]-position[0]),blindmove2[1]+(blindmove2[1]-position[1]))).occupied == None:
                        captureAnswer = True    #capture move possible
        return captureAnswer

    def isCapturePositionBlue(self,state,position): #Can the piece at position tuple perform a capture move?
        newObject2 = Board()    #new object created so that original object's values are unchanged
        newObject2.boardmatrix = copy.deepcopy(state)    #deepcopy performed to copy the object rather than the reference
        blindmove1 = newObject2.movement(topRight,(position[0],position[1]))
        blindmove2 = newObject2.movement(topLeft,(position[0],position[1]))  #blindmoves created
        captureAnswer = False
        if newObject2.checkValidLocation(blindmove1):
            if newObject2.currentLocation(blindmove1).occupied!=None and newObject2.currentLocation(blindmove1).occupied.color!=newObject2.currentLocation(position).occupied.color :
                if newObject2.checkValidLocation((blindmove1[0]+(blindmove1[0]-position[0]),blindmove1[1]+(blindmove1[1]-position[1]))):
                    if newObject2.currentLocation((blindmove1[0]+(blindmove1[0]-position[0]),blindmove1[1]+(blindmove1[1]-position[1]))).occupied == None:
                        captureAnswer= True #capture move possible
        if newObject2.checkValidLocation(blindmove2):
            if newObject2.currentLocation(blindmove2).occupied!=None and newObject2.currentLocation(blindmove2).occupied.color!=newObject2.currentLocation(position).occupied.color :
                if newObject2.checkValidLocation((blindmove2[0]+(blindmove2[0]-position[0]),blindmove2[1]+(blindmove2[1]-position[1]))):
                    if newObject2.currentLocation((blindmove2[0]+(blindmove2[0]-position[0]),blindmove2[1]+(blindmove2[1]-position[1]))).occupied == None:
                        captureAnswer = True    #capture move possible
        return captureAnswer

    def actions(self):  #returns the actions to be performed by any object in their current state(for computer)
        actions = self.legalMoves3()    #store the legal moves possible into actions array
        finalActions = []
        for action in actions:
            if action[3]-action[1] == 2:        #check if any capture move is present
                finalActions.append(action)     #add the capture move to fonal actions array
        if finalActions == []:  #if any capture move is present, capture has to be performed
            return actions
        else:
            return finalActions

    def actionsForMin(self):    #returns the actions to be performed by any object in their current state(for human)
        actionsForMin = self.legalMoves3forMin()    #store the legal moves possible into actions array
        finalActions = []
        for action in actionsForMin:
            if action[1]-action[3] == 2:     #check if any capture move is present
                finalActions.append(action)  #add the capture move to fonal actions array
        if finalActions == []:      #if any capture move is present, capture has to be performed
            return actionsForMin
        else:
            return finalActions

    def stateWithAction2(self,state,action):     #returns the state when action is performed on the state
        newObject = Board()     #deepcopy another object so that the current object's attributes are maintained
        newObject.boardmatrix = copy.deepcopy(state)    #deepcopy the attribute
        newObject.boardmatrix = newObject.movementPieceReturnsArray((action[0],action[1]),(action[2],action[3]))    #perform the action
        answer = copy.deepcopy(newObject.boardmatrix)
        newObject.boardmatrix = copy.deepcopy(state)
        return answer   #state with the performed action

    def alphaBetaSearch2(self,state,cutoff):    # alpha beta search algorithm that takes input as the current state and the cutoff for depth
        global TotalNumberOfNodes
        TotalNumberOfNodes = 1
        startingTime = time()   #variable to store the starting time of the alpha beta algorithm for the 15 seconds check
        bestMove = None     #initially the best move given by the AI is none
        bestValue = -1000   #currently alpha is -1000
        beta = 1000
        object1 = Board()   #create a new object so that the current object values are preserved
        object1.boardmatrix = copy.deepcopy(state)
        object1.boardmatrix2 = copy.deepcopy(object1.boardmatrix)
        for action in object1.actions():    #all the legal moves that can be performed in the current state
            value = object1.maxValue2(object1.stateWithAction2(state,action),bestValue,beta,startingTime,cutoff)    #value obtained by calling the MAX-VALUE function since first move is by computer
            if value>bestValue:     #to choose the action with the best value
                bestValue = value
                bestMove = action
            object1.boardmatrix = copy.deepcopy(state)  #restore the object's boardmatrix to current state at root level to perform further actions
        if bestMove == None:    #if none of the bestmove is selected- can happen in some of the ending states
            bestValue = -1000
            for action in object1.actions():
                value = object1.maxValue2(object1.stateWithAction2(state, action), bestValue, beta, startingTime,cutoff)
                #bestValue = value-1
                if value > bestValue:
                    bestValue = value
                    bestMove = action
                object1.boardmatrix = copy.deepcopy(state)
        global MinPrunes
        global MaxPrunes
        print cutoff, "Maximum Depth Cutoff"
        print MinPrunes, "MinPrunes"
        print MaxPrunes, "MaxPrunes"
        print TotalNumberOfNodes, "Total Number of nodes generated"
        MinPrunes = 0
        MaxPrunes = 0
        return bestMove

    def maxValue2(self,state,alpha,beta,time1,cutoff):  #MAX-VALUE function
        global TotalNumberOfNodes
        TotalNumberOfNodes += 1
        timeVariable = time1    #store the current time in another variable
        cutoffVariable = self.cutoff(cutoff)    #reduce the cutoff by 1 as we go lower in the tree(depth reduction)
        object1 = Board()   #create a new object
        object1.boardmatrix = copy.deepcopy(state)
        object1.boardmatrix2 = copy.deepcopy(object1.boardmatrix)
        #if object1.terminalTest() or time()-timeVariable>15 :
        if object1.terminalTest() or cutoffVariable <=0 or time()-timeVariable>15:        #check for terminal case or if the cutoff is reached
            #return object1.terminalValueCalculation()
            return object1.valueCalculation3()      #calculate the score depending ona number of factors in valueCalculation3
        value = -1000
        for action in object1.actions():    #actions available for the current state for computer
            value = max(value,object1.minValue2(object1.stateWithAction2(state,action),alpha,beta,timeVariable,cutoffVariable)) #calculate the max value and call the MIN-VALUE function
            if value>= beta:    #Max Pruning
                global MaxPrunes
                MaxPrunes += 1
                return value
            object1.boardmatrix = copy.deepcopy(state)  #restoring the boardmatrix attribute
            alpha = max(alpha,value)    #new alpha value
        return value

    def minValue2( self,state, alpha, beta,time1,cutoff):       #MIN-VALUE function
        global TotalNumberOfNodes
        TotalNumberOfNodes += 1
        timeVariable = time1    #store the current time in another variable
        cutoffVariable = self.cutoff(cutoff)    #reduce the cutoff by 1 as we go lower in the tree(depth reduction)
        object1 = Board()    #create a new object
        object1.boardmatrix = copy.deepcopy(state)
        object1.boardmatrix2 = copy.deepcopy(object1.boardmatrix)
        #if object1.terminalTest() or time()-timeVariable>15:
        if object1.terminalTest() or cutoffVariable <=0 or time() - timeVariable>15:    #check for terminal case or if the cutoff is reached
            return object1.valueCalculation3()      #calculate the score depending ona number of factors in valueCalculation3
            #return object1.terminalValueCalculation()
        value = 1000
        for action in object1.actionsForMin():  #actions available for the current state for human
            value = min(value,object1.maxValue2(object1.stateWithAction2(state,action),alpha,beta,timeVariable,cutoffVariable)) #calculate the in value and call the MAX-VALUE function
            if value <= alpha:  #Min Pruning
                global MinPrunes
                MinPrunes +=1
                return value
            object1.boardmatrix = copy.deepcopy(state)  #restoring the boardmatrix attribute
            beta = min(beta, value) #new beta value
        return value

    def cutoff(self,depth): #reducing the depth with each call
        if depth>0:
            return depth-1
        elif depth <= 0:
            return 0

    def countPieces(self):      # to determine who is the winner
        redPieces = 0
        bluePieces = 0
        for i in range(6):
            for j in range(6):
                if self.boardmatrix[i][j].occupied != None and self.boardmatrix[i][j].occupied.color == red:
                    redPieces +=1
                elif self.boardmatrix[i][j].occupied != None and self.boardmatrix[i][j].occupied.color == blue:
                    bluePieces+=1
        if redPieces-bluePieces>0:
            return 1
        elif redPieces-bluePieces <0:
            return -1
        else:
            return 0

'''The following class is the class created for handling the Graphical User Interface of the checkers game'''

class Display:
    def __init__(self):     #initial attributes
        self.captionBoard = "Checkers AI Game"      #caption
        self.fps = 60       #frames per second
        self.clockForGame = pygame.time.Clock()     #to maintain the time
        self.screenForGame = pygame.display.set_mode((450,450))     #screen size
        self.backgroundForGame = pygame.image.load('board6by6.jpg')     #background image
        self.squareSize = 75        #size for square
        self.pieceSize = 75/2       #size for pieces
        self.messageToBeDisplayed = False   #message

    def setupGUI(self):     #function to create and setup the GUI
        pygame.init()
        pygame.display.set_caption(self.captionBoard)   #set caption

    def updatingDisplay(self,boardmatrix,selectedPositionLegalMoves,selectedPiece):     #update function called within this function. To maintian the changes made in the array in the GUI
        self.screenForGame.blit(self.backgroundForGame,(0,0))   #to copy the background
        self.selectedSquare(selectedPositionLegalMoves,selectedPiece)   #to highlight the piece selected and the allowed moves for the piece
        self.drawingBoardPieces(boardmatrix)
        if self.messageToBeDisplayed:   #the messge displayed at the end
            self.screenForGame.blit(self.textDetails,self.textDetailsRect)
        pygame.display.update()
        self.clockForGame.tick(self.fps)


    def boardCoordinates(self,(xPixel,yPixel)):
        # To tell which square the selected pixel is in
        boardCoordinates = (xPixel/self.squareSize,yPixel/self.squareSize)
        return boardCoordinates

    def pixelCoordinates(self,boardCoordinates):
        #To give the centter of the square of the pixel location
        pixelCoordinates =(boardCoordinates[0]*self.squareSize+self.pieceSize,boardCoordinates[1]*self.squareSize+self.pieceSize)
        return pixelCoordinates

    def selectedSquare(self,list,point):
        #list will give an array of squares that are shown as highlighted
        for item in list:
            pygame.draw.rect(self.screenForGame,highlightedColor,(item[0]*self.squareSize,item[1]*self.squareSize,self.squareSize,self.squareSize))
        if point !=None:
            pygame.draw.rect(self.screenForGame,highlightedColor,(point[0]*self.squareSize,point[1]*self.squareSize,self.squareSize,self.squareSize))

    def drawingBoardPieces(self,checkerBoard):
        # Checker Board as an object and draws the pieces
        for i in range(6):
            for j in range(6):
                if checkerBoard.boardmatrix[i][j].occupied != None:
                    pygame.draw.circle(self.screenForGame,checkerBoard.boardmatrix[i][j].occupied.color,self.pixelCoordinates((i,j)),self.pieceSize)

    def drawingBoardSquares(self,checkerBoard):
        # Checker Board as an input and draw the squares
        for i in range(6):
            for j in range(6):
                pygame.draw.rect(self.screenForGame,checkerBoard[i][j].color,(i*self.squareSize,j*self.squareSize,self.squareSize,self.squareSize),)

    def displayMessage(self,messageToBeDisplayed):
        self.messageToBeDisplayed = True
        self.fontDetails = pygame.font.Font('comicSans.ttf',30)
        self.textDetails = self.fontDetails.render(messageToBeDisplayed,True,highlightedColor,grey)
        self.textDetailsRect = self.textDetails.get_rect()
        self.textDetailsRect.center = (225,225)

'''The following class is created for the events functionality of the Main Game. These events are used for implementing functionality in the GUI'''

class MainGame:
    def __init__(self):     #initialization
        self.display = Display()        #display object created
        self.boardMatrix = Board()      #checkers board object created
        firstChanceColor = red
        print("Enter 1 if you want to play first else enter any number")
        turnColor = input()
        if turnColor == 1:
            firstChanceColor = blue
        else:
            firstChanceColor = red
        self.turn = firstChanceColor
        #self.turn = red                 #current turn = computer
        self.selectedPiece = None       #no piece is selected currently
        self.selectedPositionLegalMoves = []    #legalmoves for the selected piece
        self.movementMadeByComputer = []    #the moves made by the computer
        self.levelRecieved = False
        self.level = 0

    def setupTheGame(self):     # function to setup a GUI
        self.display.setupGUI()

    def gameEvents(self):       #loop of the main game
        #First we try to get the location of mouse position
        self.mousePosition = self.display.boardCoordinates(pygame.mouse.get_pos())
        if self.selectedPiece !=None:
            self.selectedPositionLegalMoves = self.boardMatrix.legalMoves(self.selectedPiece)

        for currentEvent in pygame.event.get():     #events
            if self.levelRecieved == False:
                print "Please enter the level you want to play- 1,2 or 3"
                val = input()
                if val == 1:
                    self.level = 4
                    self.levelRecieved =True
                elif val == 2:
                    self.level = 12
                    self.levelRecieved = True
                elif val == 3:
                    self.levelRecieved = True
                    self.level = 20

            if self.turn == blue:       #if human's turn
                if currentEvent.type == QUIT:       #if human chooses to close the game
                    self.closeGame()
                if currentEvent.type == MOUSEBUTTONDOWN:     #if cursor moves down
                    if self.boardMatrix.currentLocation(self.mousePosition).occupied != None and self.boardMatrix.currentLocation(self.mousePosition).occupied.color == self.turn:
                        self.selectedPiece = self.mousePosition     #if human clicks on one of blue pieces
                    elif self.selectedPiece != None and self.mousePosition in self.boardMatrix.legalMoves(self.selectedPiece):  #human chooses the position to send the piece to
                        self.boardMatrix.movementPiece1(self.selectedPiece,self.mousePosition)  #perform the necessary movement
                        if self.mousePosition not in self.boardMatrix.diagonalSquareLocation(self.selectedPiece): #if the selected legal move was not in the adjacent box, this means it was a capture move
                            self.boardMatrix.pieceRemoval((self.selectedPiece[0]+(self.mousePosition[0]-self.selectedPiece[0])/2,self.selectedPiece[1]+(self.mousePosition[1]-self.selectedPiece[1])/2))
                            self.selectedPiece = self.mousePosition     #make the movement and remove the captured piece
                            self.terminateTurn()        #human's turn over
                        else:
                            self.terminateTurn()
            elif self.turn == red:      #computer's turn
                objectCopy = copy.deepcopy(self.boardMatrix)
                print "Game is analyzing the next move..."
                cutoffUsed = self.level
                self.movementMadeByComputer = self.boardMatrix.alphaBetaSearch2(objectCopy.boardmatrix,cutoffUsed)   #action given by alpha beta search
                if self.movementMadeByComputer == None:
                    actionsNoMoves = self.boardMatrix.legalMoves3()
                    actionTaken = actionsNoMoves[0]
                    self.movementMadeByComputer = actionTaken
                    self.boardMatrix.movementPiece((self.movementMadeByComputer[0], self.movementMadeByComputer[1]),(self.movementMadeByComputer[2], self.movementMadeByComputer[3]))
                else:
                    self.boardMatrix.movementPiece((self.movementMadeByComputer[0],self.movementMadeByComputer[1]),(self.movementMadeByComputer[2],self.movementMadeByComputer[3]))
                self.terminateTurn()


    def closeGame(self):    #to close the game
        pygame.quit()
        sys.exit(0)

    def updateTheGame(self):    # to call the update functions in display
        self.display.updatingDisplay(self.boardMatrix,self.selectedPositionLegalMoves,self.selectedPiece)

    def terminateTurn(self):    #to terminate turn and give the next turn to the human or computer
        if self.turn == blue:   #next move is of computer
            self.turn = red
        else:
            self.turn = blue    #next move is human
        self.selectedPiece = None
        self.selectedPositionLegalMoves = []
        count = 0
        while self.outOfMoves():        #to see if the terminal state is reached and decide who is the winner
            if self.turn == blue:
                self.turn = red
            else:
                self.turn = blue
            count = count+1
            if count>2:
                if self.boardMatrix.countPieces() == 1:
                    self.display.displayMessage("You lose!")
                elif self.boardMatrix.countPieces() == -1 :
                    self.display.displayMessage("You win!")
                elif self.boardMatrix.countPieces() == 0:
                    self.display.displayMessage("It's a Draw!")
                break

    def outOfMoves(self):       #to check if any moves left
        for i in range(6):
            for j in range(6):
                if self.boardMatrix.currentLocation((i,j)).occupied != None and self.boardMatrix.currentLocation((i,j)).occupied.color ==self.turn:
                    if self.boardMatrix.legalMoves((i,j))!=[]:
                        return False
        return True

    def main(self):
        self.setupTheGame()
        while True:
            self.gameEvents()
            self.updateTheGame()



def main():
    checkersGame = MainGame()
    checkersGame.main()

if __name__ == "__main__" :
    main()
