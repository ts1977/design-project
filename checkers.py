from graphics import *
from enum import Enum
from copy import copy, deepcopy
import unittest
import sys
import random
from model import LearningModel
from math import sqrt

class Chess:
    """initial for chess"""
    def __init__(self, x = 0, y = 0):
        self.m_x = x
        self.m_y = y
    def __str__(self):
        ss = "pos_x:" + str(self.m_x) + ", pos_y:" + str(self.m_y)
        return ss
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.m_x == self.m_x and other.m_y == self.m_y
        return False
    def set(self, x, y):
        self.m_x = x
        self.m_y = y

class Player :
    """the player class has the player's operations"""
    def __init__(self, name, startPositions):
        self.chesses = []
        self.m_kings = []
        self.edges = []
        self.guard = []
        self.being_attacked = False
        self.num_friend = 0
        self.m_name = name
        self.m_model = LearningModel()

        for pos in startPositions:
            self.chesses.append(Chess(pos[0], pos[1]))

    def __str__(self):
        ss = "Player:" + self.m_name + ", Chesses:"
        for chess in self.chesses:
            ss += str(chess)
        return ss

    def size(self):
        return len(self.chesses)

    def __len__(self):
        return len(self.chesses)

    def empty(self):
        return self.size() == 0

    def setChess(self, positions):
        self.chesses = []
        for pos in positions:
            self.chesses.append(Chess(pos[0], pos[1]))

    def moveChess(self, chessPrev, chessAfter):
        self.chesses.remove(chessPrev)
        self.chesses.append(chessAfter)
        if chessPrev in self.m_kings:
            self.m_kings.remove(chessPrev)
            self.m_kings.append(chessAfter)
        elif chessPrev not in self.m_kings and (chessAfter.m_x == 7 or chessAfter.m_x == 0):
            self.m_kings.append(chessAfter)

    # did this player lose?
    def lost(self, opp):
        if len(self) == 0:
            return True

        valid = range(8)
        for chess in self.chesses:
            if chess in self.m_kings:
                dirs = DIR_KINGS
            else:
                dirs = self.dir_pawns

            for d in dirs:
                nx = Chess(chess.m_x + d[0], chess.m_y + d[1])
                if nx.m_x in valid and nx.m_y in valid and nx not in self.chesses and nx not in opp.chesses:
                    return False

        return True

DIR_KINGS = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

class ChessBoard :
    class Status(Enum):
        INVALID = 0
        PLAIN = 1
        CAPTURE = 2
        WIN = 3

    def __init__(self, height = 700, width = 700):
        self.m_winHeight = height
        self.m_winWidth = width
        self.m_rows = 8
        self.m_cols = 8
        self.m_chessH = height/self.m_rows
        self.m_chessW = width/self.m_cols
        self.m_chessR = self.m_chessH*0.4
        self.MAX_STEPS = 3
        self.m_initBoard = [
                ['.','*','.','*','.','*','.','*'],
                ['*','.','*','.','*','.','*','.'],
                ['.','*','.','*','.','*','.','*'],
                ['*','.','*','.','*','.','*','.'],
                ['.','*','.','*','.','*','.','*'],
                ['*','.','*','.','*','.','*','.'],
                ['.','*','.','*','.','*','.','*'],
                ['*','.','*','.','*','.','*','.'],
                ]
        self.m_player1 = Player("player", [[0,1],[0,3],[0,5],[0,7],[1,0],[1,2],[1,4],[1,6],[2,1],[2,3],[2,5],[2,7]])
        self.m_player2 = Player("computer", [[5,0],[5,2],[5,4],[5,6],[6,1],[6,3],[6,5],[6,7],[7,0],[7,2],[7,4],[7,6]])

        self.m_player1.home_row = 0
        self.m_player2.home_row = 7
        self.m_player1.dir_pawns = [[1, 1], [1, -1]]
        self.m_player2.dir_pawns = [[-1, 1], [-1, -1]]
        self.m_curBoard = []
        self.m_moves_wo_capture = 0


    """display chessboard"""
    def displayBoard(self, win):
        for i in range(self.m_rows):
            for j in range(self.m_cols):
                # skip '#' board
                if self.m_initBoard[i][j] == '#':
                    continue
                cur_x = j*self.m_chessW
                cur_y = i*self.m_chessH
                box = Rectangle(Point(cur_x, cur_y), Point(cur_x+self.m_chessW, cur_y+self.m_chessH))
                if self.m_initBoard[i][j] == '*':
                    box.setFill("black")
                else:
                    box.setFill("white")
                box.draw(win)

    """display chess"""
    def displayChess(self, win):
        for chess in self.m_player1.chesses:
            circle = Circle(Point(chess.m_y*self.m_chessW + self.m_chessW/2, chess.m_x*self.m_chessH + self.m_chessH/2), self.m_chessR)
            circle.setFill("red")
            circle.draw(win)
        for chess in self.m_player2.chesses:
            circle = Circle(Point(chess.m_y*self.m_chessW + self.m_chessW/2, chess.m_x*self.m_chessH + self.m_chessH/2), self.m_chessR)
            circle.setFill("blue")
            circle.draw(win)
        for chess in self.m_player1.m_kings:
            square = Rectangle(Point(chess.m_y*self.m_chessW+0.1*self.m_chessW, chess.m_x*self.m_chessH+0.1*self.m_chessH), Point(chess.m_y*self.m_chessW+0.1*self.m_chessW+2*self.m_chessR, chess.m_x*self.m_chessH+0.1*self.m_chessH+2*self.m_chessR))
            square.setFill("red")
            square.draw(win)
        for chess in self.m_player2.m_kings:
            square = Rectangle(Point(chess.m_y*self.m_chessW+0.1*self.m_chessW, chess.m_x*self.m_chessH+0.1*self.m_chessH), Point(chess.m_y*self.m_chessW+0.1*self.m_chessW+2*self.m_chessR, chess.m_x*self.m_chessH+0.1*self.m_chessH+2*self.m_chessR))
            square.setFill("blue")
            square.draw(win)

    def displayButton(self,win):
        mode1 = Rectangle(Point(750,600), Point(950,675))
        mode2 = Rectangle(Point(750,700), Point(950,775))
        mode1.setFill("black")
        mode2.setFill("black")
        mode1.draw(win)
        mode2.draw(win)

    def displayText(self, win):
        message3 = Text(Point(850,630), 'Player vs Computer')
        message3.setTextColor('white')
        message3.setStyle('italic')
        message3.setSize(15)
        message3.draw(win)

        message = Text(Point(850,730), 'Computer vs Player')
        message.setTextColor('white')
        message.setStyle('italic')
        message.setSize(15)
        message.draw(win)

    def displayError(self, win):
        message = Text(Point(800, 100), 'Invalid move')
        message.setTextColor('red')
        message.setStyle('italic')
        message.setSize(25)
        message.draw(win)
    def displayError2(self, win):
        message = Text(Point(800, 100), 'You must jump')
        message.setTextColor('red')
        message.setStyle('italic')
        message.setSize(25)
        message.draw(win)
    def removeError(self, win):
        blank = Rectangle(Point(700,0), Point(1000,200))
        blank.setFill("white")
        blank.setOutline("white")
        blank.draw(win)

    def winText1(self, win):
        message = Text(Point(self.m_winWidth/2, self.m_winHeight/2), 'You Win')
        message.setTextColor('red')
        message.setSize(36)
        message.draw(win)

    def winText2(self, win):
        message = Text(Point(self.m_winWidth/2, self.m_winHeight/2), 'You Lost')
        message.setTextColor('red')
        message.setSize(36)
        message.draw(win)

    """set choose chess to grey"""
    def highlightChess(self, win, chess):
        if(chess in self.m_player1.m_kings or chess in self.m_player2.m_kings):
            square = Rectangle(Point(chess.m_y*self.m_chessW+0.1*self.m_chessW, chess.m_x*self.m_chessH+0.1*self.m_chessH), Point(chess.m_y*self.m_chessW+0.1*self.m_chessW+2*self.m_chessR, chess.m_x*self.m_chessH+0.1*self.m_chessH+2*self.m_chessR))
            square.setFill("gray")
            square.draw(win)
        else:
            circle = Circle(Point(chess.m_y*self.m_chessW + self.m_chessW/2, chess.m_x*self.m_chessH+self.m_chessH/2), self.m_chessR)
            circle.setFill("gray")
            circle.draw(win)

    """convert win position to chess index"""
    def position2Index(self, point):
        return point.x/self.m_chessW, point.y/self.m_chessH

    """return direction of two chess"""
    def chessDirection(self, preChess, aftChess):
        delta_x = aftChess.m_x - preChess.m_x
        if preChess in self.m_player1.m_kings:
            if delta_x > 0:
                delta_x = 1
            else: delta_x = -1
        else:
            if delta_x > 0:
                delta_x = 1
            else: delta_x = 0
        delta_y = aftChess.m_y - preChess.m_y
        if not delta_y == 0:
            delta_y = 1 if delta_y > 0 else -1
        return delta_x,delta_y

    def chessDirection2(self, preChess, aftChess):
        delta_x = aftChess.m_x - preChess.m_x
        if preChess in self.m_player2.m_kings:
            if delta_x < 0:
                delta_x = -1
            else: delta_x = 1
        else:
            if delta_x < 0:
                delta_x = -1
            else: delta_x = 0
        delta_y = aftChess.m_y - preChess.m_y
        if not delta_y == 0:
            delta_y = 1 if delta_y > 0 else -1
        return delta_x,delta_y

    """set max steps, eq to set level of AI"""
    def setMaxSteps(self, l):
        self.MAX_STEPS = l

    """apply player chesses on board"""
    def applyPlayer(self):
        self.m_curBoard = deepcopy(self.m_initBoard)
        for chess in self.m_player1.chesses:
            self.m_curBoard[chess.m_x][chess.m_y] = 'O'
        for chess in self.m_player2.chesses:
            self.m_curBoard[chess.m_x][chess.m_y] = 'X'

    # find the capture moves
    def captures(self, player1, player2):
        validRange = range(8)
        for chess in player1.chesses:
            if chess in player1.m_kings:
                directions = DIR_KINGS
            else:
                directions = player1.dir_pawns
            for d in directions:
                mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                aft = Chess(mid.m_x+d[0], mid.m_y+d[1])
                if aft not in player1.chesses and aft not in player2.chesses and aft.m_x in validRange and aft.m_y in validRange and mid in player2.chesses:
                    yield mid, chess, aft

    # find the pieces that can makes move other than capture
    def movable(self, player1, player2):
        validRange = range(8)
        for chess in player1.chesses:
            capture = False
            move = False
            if chess in player1.m_kings:
                directions = DIR_KINGS
            else:
                directions = player1.dir_pawns
            for d in directions:
                mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                aft = Chess(mid.m_x+d[0], mid.m_y+d[1])
                if aft not in player1.chesses and aft not in player2.chesses and aft.m_x in validRange and aft.m_y in validRange and mid in player2.chesses:
                    capture = True
                if mid not in player1.chesses and mid not in player2.chesses and mid.m_x in validRange and mid.m_y in validRange:
                    move = True

            if move and not capture:
                yield chess

    # is this piece a loner checker
    def is_loner(self, checker):
        for d in DIR_KINGS:
            adj = Chess(checker.m_x+d[0], checker.m_y+d[1])
            if adj in self.m_player1.chesses or adj in self.m_player2.chesses:
                return False
        return True

    # all possible (i.e. legal) moves that the player can make
    def possible_moves(self, player1, player2):
        capture_moves = list(self.captures(player1, player2))
        valid = range(8)

        if len(capture_moves) > 0:
            for m in capture_moves:
                yield m
            return

        for chess in player1.chesses:
            if chess in player1.m_kings:
                directions = DIR_KINGS
            else:
                directions = player1.dir_pawns
            for d in directions:
                nx = Chess(chess.m_x+d[0], chess.m_y+d[1])
                if nx.m_x in valid and nx.m_y in valid and nx not in player1.chesses and nx not in player2.chesses:
                    yield None, chess, nx
        return

    def can_capture(self, player1, player2):
        captures = list(self.captures(player1, player2))
        return True if captures else False

    """print chessboard"""

    def __str__(self):
        self.applyPlayer()
        str = ""
        for row in self.m_curBoard:
            str += ", ".join(row)
            str += "\n"
        return str

    """return true when there is a winner"""
    def win(self):
        if self.m_moves_wo_capture > 99:
            return True
        return self.m_player1.lost(self.m_player2) or self.m_player2.lost(self.m_player1)

    def reset(self):
        self.m_player1.setChess([[0,1],[0,3],[0,5],[0,7],[1,0],[1,2],[1,4],[1,6],[2,1],[2,3],[2,5],[2,7]])
        self.m_player2.setChess([[5,0],[5,2],[5,4],[5,6],[6,1],[6,3],[6,5],[6,7],[7,0],[7,2],[7,4],[7,6]])
        self.m_moves_wo_capture = 0

    # obtain the features for a single player
    def getPlayerData(self, player1, player2):

        def div(a, b):
            if b == 0:
                return 0
            return (a/b)

        n_pieces = 0
        n_kings = 0
        n_pawns = 0
        n_edge = 0
        n_x = 0
        n_y = 0

        for chess in player1.chesses:
            if chess.m_y == 0 or chess.m_y == 7:
                n_edge += 1

            n_pieces += 1
            if chess not in player1.m_kings:
                n_pawns += 1
            else:
                n_kings += 1

            n_x += abs(chess.m_x - player1.home_row)
            n_y += abs(chess.m_y - player1.home_row)

        data = [
                n_pawns,
                n_kings,
                n_edge,
                div(n_x, n_pieces),
                div(n_y, n_pieces)
            ]

        return data

    # get the features for both players
    def getBoardData(self, player1, player2):
        data = []
        data.extend(self.getPlayerData(player1, player2))
        data.extend(self.getPlayerData(player2, player1))
        return data

    """searches for the best move, performs recursive minimax strategy"""
    def oneStep(self, model, player1, player2, curStep):
        bestScore = None
        score = 0
        maxChessPrev = Chess()
        maxChessAft = Chess()

        myChess = player1.chesses
        oppoChess = player2.chesses
        myKings = player1.m_kings
        oppoKings = player2.m_kings

        for captured, chess, nx_chess in self.possible_moves(player1, player2):

            # apply the move
            myChess.remove(chess)
            myChess.append(nx_chess)

            if chess in myKings:
                myKings.remove(chess)
                myKings.append(nx_chess)

            if captured:
                oppoChess.remove(captured)
                if captured in oppoKings:
                    king_capture = True
                    oppoKings.remove(captured)
                else:
                    king_capture = False

            # evaluate the move
            score = model.eval(self.getBoardData(player1, player2))

            if not self.win():
                # only do minimax if the game is not over
                # and we haven't exceeded lookahead maximum
                if curStep < self.MAX_STEPS:
                    if captured:
                        # search deeper if capture move
                        [nx, _, _] = self.oneStep(model, player2, player1, curStep)
                    else:
                        [nx, _, _] = self.oneStep(model, player2, player1, curStep + 1)
                    score -= nx
            else:
                # infinite score for winning move
                score = float('inf')

            # is this the best score?
            if not bestScore or score > bestScore:
                bestScore = score
                maxChessPrev = chess
                maxChessAft = nx_chess

            # undo the move to revert to initial state
            myChess.remove(nx_chess)
            myChess.append(chess)
            if nx_chess in myKings:
                myKings.remove(nx_chess)
                myKings.append(chess)

            if captured:
                oppoChess.append(captured)
                if king_capture:
                    oppoKings.append(captured)

        # debugging, should never happen
        if bestScore is None:
            print(player1)
            print(player2)
            print(self.can_capture(player1, player2))

        return bestScore, maxChessPrev, maxChessAft


    """return status of current move"""
    def move(self, chess, nxD, myChess, oppoChess):
        # as long as two steps
        status = self.Status.PLAIN
        nx_x = chess.m_x + nxD[0]
        nx_y = chess.m_y + nxD[1]
        nx_chess = Chess(nx_x, nx_y)

        if (nx_chess in oppoChess):
            nx_x += nxD[0]
            nx_y += nxD[1]
            status = self.Status.CAPTURE
        if not self.isValid(nx_x, nx_y):
            status = self.Status.INVALID
        return status

    """move chess"""
    def moveChess(self, player, oppoChess, oppoKings,chessPrev, chessAft):
        if abs(chessAft.m_x - chessPrev.m_x) >= 2 or abs(chessAft.m_y - chessPrev.m_y) >= 2:
            # if oppo chess should be removed
            chess = Chess((chessPrev.m_x+chessAft.m_x)/2, (chessPrev.m_y+chessAft.m_y)/2)
            if chess in oppoChess:
                oppoChess.remove(chess)
            if chess in oppoKings:
                oppoKings.remove(chess)
            self.m_moves_wo_capture = 0
        else:
            self.m_moves_wo_capture += 1
        player.moveChess(chessPrev, chessAft)

    """return true if is at valid position"""
    def isValid(self,  aft_x, aft_y):
        if (aft_x < 0 or aft_x >= self.m_rows) or (aft_y < 0 or aft_y >= self.m_cols):
            return False
        chess = Chess(aft_x, aft_y)
        if (chess in self.m_player1.chesses or chess in self.m_player2.chesses):
            return False

        return self.m_initBoard[aft_x][aft_y] in ['*']
