from checkers import *

class Game:
    def __init__(self):
        self.m_chessBoard = ChessBoard()
        self.m_player1Chess = self.m_chessBoard.m_player1.chesses
        self.m_player2Chess = self.m_chessBoard.m_player2.chesses
        self.player1Kings = self.m_chessBoard.m_player1.m_kings
        self.player2Kings = self.m_chessBoard.m_player2.m_kings
        self.model = self.m_chessBoard.m_model
    def end(self):
        return self.m_chessBoard.win()
    def printChessTable(self):
        print (self.m_chessBoard)
    def printPlayerChess(self):
        print (self.m_chessBoard.m_player1)
    def printAIChess(self):
        print (self.m_chessBoard.m_player2)
    def movePlayer1Chess(self, chessPrev, chessAft):
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player1, self.m_player2Chess, self.player2Kings, chessPrev, chessAft)
    def movePlayer2Chess(self, chessPrev, chessAft):
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player2, self.m_player1Chess, self.player1Kings, chessPrev, chessAft)
    def setMaxSteps(self, s):
        self.m_chessBoard.setMaxSteps(s)
    def moveAIChess1(self,steps):
        print ("AI moving")
        [_, chessPrev, chessAft] = self.m_chessBoard.oneStep(self.m_player2Chess, self.m_player1Chess, 1)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player2, self.m_player1Chess, self.player1Kings, chessPrev, chessAft)
    def moveAIChess2(self, steps):
        print ("AI moving")
        [_, chessPrev, chessAft] = self.m_chessBoard.oneStep2(self.m_player1Chess, self.m_player2Chess, 1)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player1, self.m_player2Chess, self.player2Kings, chessPrev, chessAft)

if __name__ == '__main__':
    g = Game()
    g.setMaxSteps(3)
    chess = Chess()
    board = g.m_chessBoard
    player1Chess= board.m_player1.chesses
    player2Chess = board.m_player2.chesses
    steps = 0

    g.m_chessBoard.displayButton(win)
    g.m_chessBoard.displayText(win)

    while not g.end():
        if  steps % 2 == 0:
            g.printChessTable()
            g.printPlayerChess()
            g.printAIChess()
            g.modeAIChess2(steps)
        else:
            g.moveAIChess1(steps)
        steps += 1
        g.model.logmove(g.m_chessBoard.getBoardData())

    g.model.analyze_result()
