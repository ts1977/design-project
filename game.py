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
# def playGame():

if __name__ == '__main__':
    g = Game()
    g.setMaxSteps(3)
    chess = Chess()
    board = g.m_chessBoard
    player1Chess= board.m_player1.chesses
    player2Chess = board.m_player2.chesses
    steps = 0
    win = GraphWin('Checkers', 1000, 1000)
    
    g.m_chessBoard.displayButton(win)
    g.m_chessBoard.displayText(win)

    select = win.getMouse()
    while not (select.x >= 750 and select.x <= 950) and ((select.y >= 600 and select.y <= 675) or (select.y >= 700 and select.y <= 775) or (select.y >= 800 and select.y <= 875)):
        select = win.getMouse()

    if select.y >= 600 and select.y <= 675:
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
                
                preChess = Chess(int(j), int(i))
                if not preChess in player1Chess:
                    continue
                g.m_chessBoard.highlightChess(win, preChess) 
                [i, j] = g.m_chessBoard.position2Index(win.getMouse())
                aftChess = Chess(int(j), int(i))
                [delta_x, delta_y] = g.m_chessBoard.chessDirection(preChess, aftChess)
                if delta_x == 0 or not g.m_chessBoard.isValid(aftChess.m_x, aftChess.m_y) or (aftChess.m_x - preChess.m_x)>2 or abs(aftChess.m_y - preChess.m_y)> 2 :
                    g.m_chessBoard.displayError(win)
                    continue
                else:
                    g.m_chessBoard.removeError(win)
                status = board.move(preChess, [delta_x, delta_y], player1Chess, player2Chess)
                # status = board.move(preChess, aftChess, playerChess, oppoChess)
                capturePrev, captureAft = g.m_chessBoard.test_capture_player1()
                if capturePrev.m_x != -1:
                    if  status != g.m_chessBoard.Status.CAPTURE:
                        status = board.move(preChess, [delta_x, delta_y], player1Chess, player2Chess)
                        g.m_chessBoard.displayError2(win)
                        continue
                    else:
                        g.movePlayer1Chess(preChess, Chess(preChess.m_x+delta_x*2, preChess.m_y+delta_y*2))
                        g.m_chessBoard.removeError(win)
                else:
                    if status == g.m_chessBoard.Status.PLAIN:
                        g.movePlayer1Chess(preChess, Chess(preChess.m_x+delta_x, preChess.m_y+delta_y))               
                    else:
                        print ("Invalid move")
            else:
                g.moveAIChess1(steps)
            steps += 1


    elif select.y >= 700 and select.y <= 775:
        while not g.end():
            win.autoflush = False
            g.m_chessBoard.displayBoard(win)
            g.m_chessBoard.displayChess(win)
            g.m_chessBoard.displayButton(win)
            g.m_chessBoard.displayText(win)
            win.autoflush = True

            if  steps % 2 == 1:
                g.printChessTable()
                g.printPlayerChess()
                g.printAIChess()           
                [i, j] = g.m_chessBoard.position2Index(win.getMouse())
                position = Point(i* board.m_chessH, j* board.m_chessW)
                
                preChess = Chess(int(j), int(i))
                if not preChess in player2Chess:
                    continue
                g.m_chessBoard.highlightChess(win, preChess) 
                [i, j] = g.m_chessBoard.position2Index(win.getMouse())
                aftChess = Chess(int(j), int(i))
                [delta_x, delta_y] = g.m_chessBoard.chessDirection2(preChess, aftChess)
                if delta_x == 0 or not g.m_chessBoard.isValid(aftChess.m_x, aftChess.m_y) or (aftChess.m_x - preChess.m_x) < -2 or abs(aftChess.m_y - preChess.m_y) > 2 :
                    g.m_chessBoard.displayError(win)
                    continue
                else:
                    g.m_chessBoard.removeError(win)
                status = board.move(preChess, [delta_x, delta_y], player2Chess, player1Chess)
                # status = board.move(preChess, aftChess, playerChess, oppoChess)
                
                capturePrev, captureAft = g.m_chessBoard.test_capture_player2()
                if capturePrev.m_x != -1:
                    if  status != g.m_chessBoard.Status.CAPTURE:
                        status = board.move(preChess, [delta_x, delta_y], player2Chess, player1Chess)
                        g.m_chessBoard.displayError2(win)
                        continue
                    else:
                        g.movePlayer2Chess(preChess, Chess(preChess.m_x+delta_x*2, preChess.m_y+delta_y*2))
                        g.m_chessBoard.removeError(win)
                else:
                    if status == g.m_chessBoard.Status.PLAIN:
                        g.movePlayer2Chess(preChess, Chess(preChess.m_x+delta_x, preChess.m_y+delta_y))               
                    else:
                        print ("Invalid move")
            else:
                g.moveAIChess2(steps)
            steps += 1

    elif select.y >= 800 and select.y <= 875:
        while not g.end():
            win.autoflush = False
            g.m_chessBoard.displayBoard(win)
            g.m_chessBoard.displayChess(win)
            g.m_chessBoard.displayButton(win)
            g.m_chessBoard.displayText(win)
            win.autoflush = True

            if steps%2 == 0:
                g.printChessTable()
                g.printPlayerChess()
                g.printAIChess()
                g.moveAIChess2(steps)
            else:
                g.moveAIChess1(steps)
            steps += 1

    if len(g.m_chessBoard.m_player1.chesses) == 0:
        g.m_chessBoard.winText2(win)
    else:
        g.m_chessBoard.winText1(win)
    win.getMouse()
    win.close()
