from checkers import *
from tkinter import *
class Game:
    def __init__(self):
        self.m_chessBoard = ChessBoard()
        self.m_player1Chess = self.m_chessBoard.m_player1.chesses
        self.m_player2Chess = self.m_chessBoard.m_player2.chesses
        self.player1Kings = self.m_chessBoard.m_player1.m_kings
        self.player2Kings = self.m_chessBoard.m_player2.m_kings
    def end(self):
        return self.m_chessBoard.win()
    def printChessTable(self):
        print (self.m_chessBoard)
    def printPlayerChess(self):
        print (self.m_chessBoard.m_player1)
    def printAIChess(self):
        print (self.m_chessBoard.m_player2)
    def movePlayerChess(self, chessPrev, chessAft):
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player1, self.m_player2Chess, self.player2Kings, chessPrev, chessAft)
    def setMaxSteps(self, s):
        self.m_chessBoard.setMaxSteps(s)
    def moveAIChess1(self,steps):
        print ("AI moving")
        [_, chessPrev, chessAft] = self.m_chessBoard.oneStep(self.m_player2Chess, self.m_player1Chess, 1)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player2, self.m_player1Chess, self.player1Kings, chessPrev, chessAft)
    def moveAIChess2(self, steps):
        print ("AI moving")
        [_, chessPrev, chessAft] = self.m_chessBoard.oneStep(self.m_player1Chess, self.m_player2Chess, 1)
        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(self.m_chessBoard.m_player1, self.m_player2Chess, self.player2Kings, chessPrev, chessAft)
# def playGame():
    
if __name__ == '__main__':
    g = Game()
    g.setMaxSteps(3)
    chess = Chess()
    board = g.m_chessBoard
    playerChess= board.m_player1.chesses
    oppoChess = board.m_player2.chesses
    steps = 0
    win = GraphWin('Checkers', 1000, 1000)
    
    g.m_chessBoard.displayButton(win)
    g.m_chessBoard.displayText(win)

    pos = win.getMouse()
    while not pos.x >= 400 and pos.x <= 600 and pos.y >= 800 and pos.y <= 900:
        pos = win.getMouse()


    while not g.end():
        win.autoflush = False
        g.m_chessBoard.displayBoard(win)
        g.m_chessBoard.displayChess(win)
        g.m_chessBoard.displayButton(win)
        g.m_chessBoard.displayText(win)
        win.autoflush = True

        if  steps % 2 == 0:
            g.printChessTable()
            g.printPlayerChess()
            g.printAIChess()

            
            [i, j] = g.m_chessBoard.position2Index(win.getMouse())
            position = Point(i* board.m_chessH, j* board.m_chessW)
            # if position.x >= 400 and position.x <= 600 and position.y >= 800 and position.y <= 900:
            #     g.m_chessBoard.reset()
            #     steps = 0
            #     continue
            preChess = Chess(int(j), int(i))
            if not preChess in playerChess:
                continue
            g.m_chessBoard.highlightChess(win, preChess) 
            [i, j] = g.m_chessBoard.position2Index(win.getMouse())
            aftChess = Chess(int(j), int(i))
            [delta_x, delta_y] = g.m_chessBoard.chessDirection(preChess, aftChess)
            if delta_x == 0 or not g.m_chessBoard.isValid(aftChess.m_x, aftChess.m_y) or (aftChess.m_x - preChess.m_x)>1 or (aftChess.m_y - preChess.m_y)>1 :
                g.m_chessBoard.displayError(win)
                continue
            else:
                g.m_chessBoard.removeError(win)
            status = board.move(preChess, [delta_x, delta_y], playerChess, oppoChess)
            # status = board.move(preChess, aftChess, playerChess, oppoChess)
            
            if g.m_chessBoard.test_capture_player1() == True:
                if  status != g.m_chessBoard.Status.CAPTURE:
                    status = board.move(preChess, [delta_x, delta_y], playerChess, oppoChess)
                    g.m_chessBoard.displayError2(win)
                    continue
                else:
                    g.movePlayerChess(preChess, Chess(preChess.m_x+delta_x*2, preChess.m_y+delta_y*2))
                    g.m_chessBoard.removeError(win)
            else:
                if status == g.m_chessBoard.Status.PLAIN:
                    g.movePlayerChess(preChess, Chess(preChess.m_x+delta_x, preChess.m_y+delta_y))               
                else:
                    print ("Invalid move")
        else:
            g.moveAIChess1(steps)
        steps += 1
        
    # g.m_chessBoard.displayBoard(win)
    # g.m_chessBoard.displayChess(win)
    # g.m_chessBoard.displayButton(win)
    # g.m_chessBoard.displayText(win)
    if len(g.m_chessBoard.m_player1.chesses) == 0:
        g.m_chessBoard.winText2(win)
    else:
        g.m_chessBoard.winText1(win)
    win.getMouse()
    win.close()
