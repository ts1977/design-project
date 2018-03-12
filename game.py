from checkers import *
from tkinter import *
class Game:
    def __init__(self):
        self.m_chessBoard = ChessBoard()
        self.m_playerChess = self.m_chessBoard.m_player1.m_chesses
        self.m_aiChess = self.m_chessBoard.m_player2.m_chesses
    def end(self):
        return self.m_chessBoard.win()
    def printChessTable(self):
        print (self.m_chessBoard)
    def printPlayerChess(self):
        print (self.m_chessBoard.m_player1)
    def printAIChess(self):
        print (self.m_chessBoard.m_player2)
    def movePlayerChess(self, chessPrev, chessAft):
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player1, self.m_aiChess, chessPrev, chessAft)
    def setMaxSteps(self, s):
        self.m_chessBoard.setMaxSteps(s)
    def moveAIChess(self):
        print ("AI moving")
        [_, chess, chessAft] = self.m_chessBoard.oneStep(self.m_aiChess, self.m_playerChess, 1)
        print "moving " + str(chess) + ", to" + str(chessAft)
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player2, self.m_playerChess, chess, chessAft)

if __name__ == '__main__':
    g = Game()
    g.setMaxSteps(3)
    board = g.m_chessBoard
    playerChess= board.m_player1.m_chesses
    oppoChess = board.m_player2.m_chesses
    steps = 0
    win = GraphWin('Game', 1000, 1000)
    # [x,y] = Point(win.getMouse())
    #         if(x > 100 and x < 300 and y > 800 and y < 900):
    #win.setBackGround("Green")
    while not g.end():
        win.autoflush = False
        g.m_chessBoard.displayBoard(win)
        g.m_chessBoard.displayChess(win)
        g.m_chessBoard.displayButton(win)
        g.m_chessBoard.displayText(win)
        #win.flush()
        win.autoflush = True
        if  steps % 2 == 0:
            g.printChessTable()
            g.printPlayerChess()
            g.printAIChess()
            #[x,y] = Point(win.getMouse())
            # if(x > 100 and x < 300 and y > 800 and y < 900):
            [i, j] = g.m_chessBoard.position2Index(win.getMouse())

            preChess = Chess(j, i)
            if not preChess in playerChess:
                continue
            g.m_chessBoard.highlightChess(win, preChess) 
            [i, j] = g.m_chessBoard.position2Index(win.getMouse())
            aftChess = Chess(j, i)
            [delta_x, delta_y] = g.m_chessBoard.chessDirection(preChess, aftChess)
            if(delta_x == 0):
                g.m_chessBoard.displayError(win)
                continue
            else:
                g.m_chessBoard.removeError(win)
            status = board.move(preChess, [delta_x, delta_y], playerChess, oppoChess)
            # status = board.move(preChess, aftChess, playerChess, oppoChess)
            if status == g.m_chessBoard.Status.PLAIN:
                g.movePlayerChess(preChess, Chess(preChess.m_x+delta_x, preChess.m_y+delta_y))
            elif status == g.m_chessBoard.Status.CAPTURE:
                g.movePlayerChess(preChess, Chess(preChess.m_x+delta_x*2, preChess.m_y+delta_y*2))
            else:
                print ("Invalid move")
        else:
            g.moveAIChess()
        steps += 1
