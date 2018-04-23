

from graphics import *

from enum import Enum
from copy import copy, deepcopy
import unittest
import sys

p_piece = 1.0
p_king = 100.0
p_edge = 30.0
p_neighbor= 1.0
p_capture = 5.0

a_piece = 1.0
a_king = 100.0
a_edge = 30.0
a_neighbor= 1.0
a_capture = 5.0

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
        for pos in startPositions:
            self.chesses.append(Chess(pos[0], pos[1]))

    def __str__(self):
        ss = "Player:" + self.m_name + ", Chesses:"
        for chess in self.chesses:
            ss += str(chess)
        return ss

    def size(self):
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
        if chessAfter.m_x == 7 or chessAfter.m_x == 0:
            self.m_kings.append(chessAfter)

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
        self.m_curBoard = []


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

    # def displayChess2(self, win):
    #     for chess in self.m_player1.chesses:
    #         circle = Circle(Point(chess.m_y*self.m_chessW + self.m_chessW/2, chess.m_x*self.m_chessH + self.m_chessH/2), self.m_chessR) 
    #         circle.setFill("blue")
    #         circle.draw(win)
    #     for chess in self.m_player2.chesses:
    #         circle = Circle(Point(chess.m_y*self.m_chessW + self.m_chessW/2, chess.m_x*self.m_chessH + self.m_chessH/2), self.m_chessR) 
    #         circle.setFill("red")
    #         circle.draw(win)
    #     for chess in self.m_player1.m_kings:
    #         square = Rectangle(Point(chess.m_y*self.m_chessW+0.1*self.m_chessW, chess.m_x*self.m_chessH+0.1*self.m_chessH), Point(chess.m_y*self.m_chessW+0.1*self.m_chessW+2*self.m_chessR, chess.m_x*self.m_chessH+0.1*self.m_chessH+2*self.m_chessR))
    #         square.setFill("blue")
    #         square.draw(win)
    #     for chess in self.m_player2.m_kings:
    #         square = Rectangle(Point(chess.m_y*self.m_chessW+0.1*self.m_chessW, chess.m_x*self.m_chessH+0.1*self.m_chessH), Point(chess.m_y*self.m_chessW+0.1*self.m_chessW+2*self.m_chessR, chess.m_x*self.m_chessH+0.1*self.m_chessH+2*self.m_chessR))
    #         square.setFill("red")
    #         square.draw(win)    
    def displayButton(self,win):
        rectangle = Rectangle(Point(100,800), Point(300,900))
        rectangle2 = Rectangle(Point(400, 800), Point(600,900))
        mode1 = Rectangle(Point(750,600), Point(950,675))        
        mode2 = Rectangle(Point(750,700), Point(950,775))       
        mode3 = Rectangle(Point(750,800), Point(950,875))       
        rectangle.setFill("Green")
        rectangle2.setFill("Red")
        mode1.setFill("black")
        mode2.setFill("black")
        mode3.setFill("black")
        rectangle.draw(win)
        rectangle2.draw(win)
        mode1.draw(win)
        mode2.draw(win)
        mode3.draw(win)

    def displayText(self, win):
        message = Text(Point(200,850), 'Begin')
        message.setTextColor('black')
        message.setStyle('italic')
        message.setSize(25)
        message.draw(win)

        message2 = Text(Point(500,850), 'Reset')
        message2.setTextColor('black')
        message2.setStyle('italic')
        message2.setSize(25)
        message2.draw(win)
        
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

        message = Text(Point(850,830), 'Computer vs Computer')
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
        message = Text(Point(self.m_winWidth/2, self.m_winHeight/2), 'Player1 Wins')
        message.setTextColor('red')
        message.setSize(40)
        message.draw(win)

    def winText2(self, win):
        message = Text(Point(self.m_winWidth/2, self.m_winHeight/2), 'Player2 Wins')
        message.setTextColor('red')
        message.setSize(40)
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
        if preChess in self.m_player1.m_kings:
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

    def test_capture_player1(self):
        dir_player = [[1,-1],[1,1]]
        dir_king_player = [[1,-1],[1,1],[-1,1],[-1,-1]]
        validRange = range(8)
        for chess in self.m_player1.chesses:
            if chess in self.m_player1.m_kings:
                for d in dir_king_player:
                    mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                    aft = Chess(mid.m_x+d[0], mid.m_y+d[1])
                    if aft not in self.m_player1.chesses and aft not in self.m_player2.chesses and aft.m_x in validRange and aft.m_y in validRange and mid in self.m_player2.chesses :
                        return chess, aft
            else:
                for d in dir_player:
                    mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                    aft = Chess(mid.m_x+d[0], mid.m_y+d[1])

                    if aft not in self.m_player1.chesses and aft not in self.m_player2.chesses and aft.m_x in validRange and aft.m_y in validRange and mid in self.m_player2.chesses :
                        return chess, aft
        return Chess(-1,-1), Chess(-1,-1)

    def test_capture_player2(self):
        dir_ai = [[-1,-1],[-1,1]]
        dir_king_ai = [[1,-1],[1,1],[-1,1],[-1,-1]]
        validRange = range(8)
        for chess in self.m_player2.chesses:
            if chess in self.m_player2.m_kings:
                for d in dir_king_ai:
                    mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                    aft = Chess(mid.m_x+d[0], mid.m_y+d[1])
                    if aft.m_x in validRange and aft.m_y in validRange and aft not in self.m_player1.chesses and aft not in self.m_player2.chesses and mid in self.m_player1.chesses :
                        return chess,aft
            else:
                for d in dir_ai:
                    mid = Chess(chess.m_x+d[0], chess.m_y+d[1])
                    aft = Chess(mid.m_x+d[0], mid.m_y+d[1])
                    if aft.m_x in validRange and aft.m_y in validRange and aft not in self.m_player1.chesses and aft not in self.m_player2.chesses and mid in self.m_player1.chesses :
                        return chess, aft
        return Chess(-1,-1), Chess(-1,-1)
    """print chessboard"""

    def __str__(self):
        self.applyPlayer()
        str = ""
        for row in self.m_curBoard:
            str += ", ".join(row)
            str += "\n"
        return str

    # def selectMode(self, pos):
        # if pos.x


    """return true when there is a winner"""
    def win(self):
        self.applyPlayer()
        return self.m_player1.size() == 0 or self.m_player2.size() == 0

    

    def reset(self):
        self.m_player1.chesses = [[0,1],[0,3],[0,5],[0,7],[1,0],[1,2],[1,4],[1,6],[2,1],[2,3],[2,5],[2,7]]
        self.m_player2.chesses = [[5,0],[5,2],[5,4],[5,6],[6,1],[6,3],[6,5],[6,7],[7,0],[7,2],[7,4],[7,6]]

    def getScore(self):

        score_player = 0.0
        score_ai = 0.0

        num_chess1 = 0
        num_king1 = 0
        num_edge1 = 0
        num_neigh1 = 0
        num_capture1 = 0

        num_chess2 = 0
        num_king2 = 0
        num_edge2 = 0
        num_neigh2 = 0
        num_capture2 = 0

        num_piece1 = len(self.m_player1.chesses)
        num_piece2 = len(self.m_player2.chesses)

        dirs = [[1,1],[1,-1],[-1,1],[-1,-1]]

        for chess in self.m_player2.chesses:
            if chess in self.m_player2.m_kings:
                num_king2 += 1
            if chess in self.m_player2.edges:
                num_edge2 += 1
            for d in dirs:
                neighbor = Chess(chess.m_x + d[0], chess.m_y + d[1])
                if neighbor in self.m_player2.chesses:
                    num_neigh2 += 1
            if self.test_capture_player2():
                num_capture2 = 1
            
        score_ai = num_chess2*a_piece + num_king2*a_king + num_edge2*a_edge + num_neigh2*a_neighbor + num_capture2*a_capture

        for chess in self.m_player1.chesses:
            if chess in self.m_player1.m_kings:
                num_king1 += 1
            if chess in self.m_player1.edges:
                num_edge1 += 1
            for d in dirs:
                neighbor = Chess(chess.m_x + d[0], chess.m_y + d[1])
                if neighbor in self.m_player1.chesses:
                    num_neigh1 += 1
            if self.test_capture_player1():
                num_capture1 = 1

        score_player = num_chess1*p_piece + num_king1*p_king + num_edge1*p_edge + num_neigh1*p_neighbor + num_capture1*p_capture

        return score_ai - score_player

    # extract features from myChess wrt oppoChess
    def extract_my_features(self, myChess, oppoChess):
        x = []

        x.append(len(myChess))
        x.append(len(oppoChess))

        x.append(len(myChess.m_kings))
        x.append(len(oppoChess.m_kings))

        n_threatened = 0
        # For now, just consider a piece threatened
        # if the oppoenent has an adjacent piece that can
        # do a jump
        for chess in oppoChess:
            if chess in oppoChess.m_kings:
                dirs = [[1,1],[1,-1],[-1,1],[-1,-1]]
            else:
                dirs = [[-1,-1], [-1,1]]
            for d in dirs:
                dx = d[0]
                dy = d[1]
                move = Chess(chess.m_x + dx, chess.m_y + dy)
                if move in myChess:
                    n_threatened += 1

        x.append(n_threatened)

        n_threatened = 0
        # For now, just consider a piece threatened
        # if the oppoenent has an adjacent piece that can
        # do a jump
        for chess in myChess:
            if chess in myChess.m_kings:
                dirs = [[1,1],[1,-1],[-1,1],[-1,-1]]
            else:
                dirs = [[-1,-1], [-1,1]]
            for d in dirs:
                dx = d[0]
                dy = d[1]
                move = Chess(chess.m_x + dx, chess.m_y + dy)
                if move in oppoChess:
                    n_threatened += 1

        x.append(n_threatened)

        return x

    def reverseMove(self, myChess, oppoChess, chessPrev, chessAft, remove_oppo, d):
        # remove the previous move and restore to previous condition
        myChess.remove(chessAft)
        myChess.append(chessPrev)
        if remove_oppo:
            oppoChess.append(Chess(chessPrev.m_x + d[0], chessPrev.m_y + d[1]))

    def oneStep(self, myChess, oppoChess, curStep, alpha = -100000, beta = 100000):
        bestScore = -10000 if curStep%2 == 1 else 10000
        captureScore = -int(bestScore * 0.1)
        winScore = -int(bestScore * 0.3)
        maxChessPrev = Chess()
        maxChessAft = Chess()

        remove_oppo = False
        remove_king = False
        remove_edge = False

        dir_chess = [[-1,-1], [-1,1]]
        dir_king = [[1,1],[1,-1],[-1,1],[-1,-1]]
        capturePrev, captureAft =  self.test_capture_player2()
        if capturePrev.m_x != -1 :
            return 0, capturePrev, captureAft
        # iterate all chess
        for chess in myChess:
            # iterate all directions
            if chess in self.m_player2.m_kings:
                directions = dir_king
            else: directions = dir_chess
            for d in directions:
                nx_status = self.move(chess, d, myChess, oppoChess)
                nx_score = 0
                nx_chess = Chess(chess.m_x + d[0]*1, chess.m_y + d[1]*1)
                
                if (nx_status == self.Status.INVALID):
                    continue
                myChess.remove(chess)
                myChess.append(nx_chess)
                # if nx_chess.m_x  == 0 and chess in self.m_player2.chesses:
                #     self.m_player2.m_kings.append(nx_chess)
                if self.win():
                    # reverse move
                    self.reverseMove(myChess, oppoChess, chess, nx_chess, remove_oppo, d)
                    return winScore, nx_chess, chess

                # add score if this move make chess closer to enemy castle
                if curStep == self.MAX_STEPS:
                    nx_score += self.getScore()

                # get score
                [tmp_nx, _, _] = self.oneStep(oppoChess, myChess, curStep + 1, alpha, beta) if curStep <= self.MAX_STEPS else [nx_score,0,0]
                nx_score += tmp_nx
                # reverse move
                self.reverseMove(myChess, oppoChess, chess, nx_chess, remove_oppo, d)

                # alphat-beta early return
                if curStep%2 == 1:
                    # AI move (maximizer)
                    if nx_score > bestScore:
                        bestScore = nx_score
                        maxChessPrev = chess
                        maxChessAft = nx_chess
                    alpha = max(alpha, bestScore)
                else:
                    # player move (minimizer)
                    if nx_score < bestScore:
                        bestScore = nx_score
                        maxChessPrev = chess
                        maxChessAft = nx_chess
                    beta = min(beta, bestScore)
                if alpha >= beta:
                    return bestScore, maxChessPrev, maxChessAft
        return bestScore, maxChessPrev, maxChessAft
    
    def oneStep2(self, myChess, oppoChess, curStep, alpha = -100000, beta = 100000):
        bestScore = -10000 if curStep%2 == 1 else 10000
        captureScore = -int(bestScore * 0.1)
        winScore = -int(bestScore * 0.3)
        maxChessPrev = Chess()
        maxChessAft = Chess()

        remove_oppo = False
        remove_king = False
        remove_edge = False

        dir_chess = [[1,-1], [1,1]]
        dir_king = [[1,1],[1,-1],[-1,1],[-1,-1]]
        capturePrev, captureAft =  self.test_capture_player1()
        if capturePrev.m_x != -1 :
            return 0, capturePrev, captureAft
        # iterate all chess
        for chess in myChess:
            # iterate all directions
            if chess in self.m_player1.m_kings:
                directions = dir_king
            else: directions = dir_chess
            for d in directions:
                nx_status = self.move(chess, d, myChess, oppoChess)
                nx_score = 0
                nx_chess = Chess(chess.m_x + d[0]*1, chess.m_y + d[1]*1)
                
                if (nx_status == self.Status.INVALID):
                    continue
                myChess.remove(chess)
                myChess.append(nx_chess)
                # if nx_chess.m_x  == 0 and chess in self.m_player2.chesses:
                #     self.m_player2.m_kings.append(nx_chess)
                if self.win():
                    # reverse move
                    self.reverseMove(myChess, oppoChess, chess, nx_chess, remove_oppo, d)
                    return winScore, nx_chess, chess

                # add score if this move make chess closer to enemy castle
                if curStep == self.MAX_STEPS:
                    nx_score += self.getScore()

                # get score
                [tmp_nx, _, _] = self.oneStep(oppoChess, myChess, curStep + 1, alpha, beta) if curStep <= self.MAX_STEPS else [nx_score,0,0]
                nx_score += tmp_nx
                # reverse move
                self.reverseMove(myChess, oppoChess, chess, nx_chess, remove_oppo, d)

                # alphat-beta early return
                if curStep%2 == 1:
                    # AI move (maximizer)
                    if nx_score > bestScore:
                        bestScore = nx_score
                        maxChessPrev = chess
                        maxChessAft = nx_chess
                    alpha = max(alpha, bestScore)
                else:
                    # player move (minimizer)
                    if nx_score < bestScore:
                        bestScore = nx_score
                        maxChessPrev = chess
                        maxChessAft = nx_chess
                    beta = min(beta, bestScore)
                if alpha >= beta:
                    return bestScore, maxChessPrev, maxChessAft
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
        player.moveChess(chessPrev, chessAft)
    def moveChess2(self, player, oppoChess, oppoKings, chessPrev, chessAft):
        if abs(chessAft.m_x - chessPrev.m_x) >= 2 or abs(chessAft.m_y - chessPrev.m_y) >= 2:
            # if oppo chess should be removed
            chess = Chess((chessPrev.m_x+chessAft.m_x)/2, (chessPrev.m_y+chessAft.m_y)/2)
            if chess in oppoChess:
                oppoChess.remove(chess)
            if chess in oppoKings:
                oppoKings.remove(chess)
        player.moveChess(chessPrev, chessAft)
    """return true if is at valid position"""
    def isValid(self,  aft_x, aft_y):
        if (aft_x < 0 or aft_x >= self.m_rows) or (aft_y < 0 or aft_y >= self.m_cols):
            return False
        chess = Chess(aft_x, aft_y)
        if (chess in self.m_player1.chesses or chess in self.m_player2.chesses):
            return False

        return self.m_initBoard[aft_x][aft_y] in ['*']

