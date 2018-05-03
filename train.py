from checkers import *
import numpy as np

class Game:
    def __init__(self):
        self.m_chessBoard = ChessBoard()
        self.player1 = self.m_chessBoard.m_player1
        self.player2 = self.m_chessBoard.m_player2
        self.m_player1Chess = self.m_chessBoard.m_player1.chesses
        self.m_player2Chess = self.m_chessBoard.m_player2.chesses
        self.player1Kings = self.m_chessBoard.m_player1.m_kings
        self.player2Kings = self.m_chessBoard.m_player2.m_kings
        self.model1 = self.m_chessBoard.m_player1.m_model
        self.model2 = self.m_chessBoard.m_player2.m_model
    def end(self):
        return self.m_chessBoard.win()
    def printChessTable(self):
        print (self.m_chessBoard)
    def printPlayerChess(self):
        print (self.m_chessBoard.m_player1)
    def printAIChess(self):
        print (self.m_chessBoard.m_player2)
    def setMaxSteps(self, s):
        self.m_chessBoard.setMaxSteps(s)
    def moveAIChess1(self,steps):
        print ("AI moving")
        [score, chessPrev, chessAft] = self.m_chessBoard.oneStep(self.model1, self.player1, self.player2, 1)
        print("score = ", score)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.player1, self.m_player2Chess, self.player2Kings, chessPrev, chessAft)
    def moveAIChess2(self, steps):
        print ("AI moving")
        [score, chessPrev, chessAft] = self.m_chessBoard.oneStep(self.model2, self.player2, self.player1, 1)
        print("score = ", score)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.player2, self.m_player1Chess, self.player1Kings, chessPrev, chessAft)


def play():
    g = Game()
    g.setMaxSteps(3)
    board = g.m_chessBoard
    steps = 0

    g.model1.reload_model()
    g.model2.mutate(g.model1)

    while not g.end():
        g.printChessTable()
        g.printPlayerChess()
        g.printAIChess()
        if  steps % 2 == 0:
            g.moveAIChess1(steps)
        else:
            g.moveAIChess2(steps)
        steps += 1
        g.model1.logmove(g.m_chessBoard.getBoardData(g.player1, g.player2))

    g.model1.analyze_result()
    return g.model1

if __name__ == '__main__':
    norms = []
    m = play()
    for _ in range(40):
        nm = play()
        norm = np.linalg.norm(m.w - nm.w)
        norms.append(norm)

    print(norms)

