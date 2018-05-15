"""
Use the GUI to play Computer

Arguments:

    --model: takes an argument which select a model file
             to load for the opponent

            For example, given a file x1.h5 in the 'save'
            directory use, --model x1, without .h5 extension

            By default, will use file it will used model1

            We have included a bunch of pretrained models
            in the save directory that can be tested.

    --train: optional, takes no arguments
             Indicates that you want the AI to be trained
             on the outcome of the game.
"""

from checkers import *
import time
import argparse

class Game:
    def __init__(self):
        self.m_chessBoard = ChessBoard()
        self.board = self.m_chessBoard
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

    def moveAI(self, player, opp):
        state = self.board.getBoardData(player, opp)

        [score, chessPrev, chessAft] = self.m_chessBoard.oneStep(player.m_model, player, opp, 1)
        print("score = ", score)

        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(player, opp.chesses, opp.m_kings, chessPrev, chessAft)

        next_state = self.board.getBoardData(player, opp)

        reward = len(player)-len(opp)
        done = self.end()

        if done:
            if player.lost(opp):
                reward = -12
            elif opp.lost(player):
                reward = 12
            else:
                reward = -2

        player.m_model.remember(state, reward, next_state, done)

# prompt user if he want to play first or second
def first_or_second(board, win):
    board.displayButton(win)
    board.displayText(win)

    select = win.getMouse()
    while True:
        if select.y >= 600 and select.y <= 675:
            return False
        elif select.y >= 700 and select.y <= 775:
            return True

        select = win.getMouse()

def play(model, train):
    g = Game()
    board = g.m_chessBoard
    g.setMaxSteps(3)
    chess = Chess()
    win = GraphWin('Checkers', 1000, 1000)
    steps = 0

    second = first_or_second(board, win)

    if second:
        human = g.player2
        mach  = g.player1
    else:
        human = g.player1
        mach  = g.player2

    f = './save/{}'.format(model)
    mach.m_model.load(f)

    while not g.end():
        win.autoflush = False
        board.displayBoard(win)
        board.displayChess(win)
        board.displayButton(win)
        board.displayText(win)
        win.autoflush = True

        if  steps % 2 == int(second):
            # human players turn
            # grab mouse input, and apply the move

            g.printChessTable()
            g.printPlayerChess()
            g.printAIChess()

            [i, j] = board.position2Index(win.getMouse())
            position = Point(i* board.m_chessH, j* board.m_chessW)
            preChess = Chess(int(j), int(i))
            if not preChess in human.chesses:
                continue
            board.highlightChess(win, preChess)
            [i, j] = board.position2Index(win.getMouse())
            aftChess = Chess(int(j), int(i))

            if second:
                [delta_x, delta_y] = board.chessDirection2(preChess, aftChess)
            else:
                [delta_x, delta_y] = board.chessDirection(preChess, aftChess)

            if (delta_x == 0 or
                not board.isValid(aftChess.m_x, aftChess.m_y) or
                abs(aftChess.m_y - preChess.m_y)> 2 or
                (not second and (aftChess.m_x - preChess.m_x) > 2) or
                (second and (aftChess.m_x - preChess.m_x) < -2)):
                board.displayError(win)
                continue

            board.removeError(win)
            status = board.move(preChess, [delta_x, delta_y], human.chesses, mach.chesses)

            if board.can_capture(human, mach):
                if  status != g.m_chessBoard.Status.CAPTURE:
                    status = board.move(preChess, [delta_x, delta_y], human.chesses, mach.chesses)
                    g.m_chessBoard.displayError2(win)
                    continue
                else:
                    aft = Chess(preChess.m_x+delta_x*2, preChess.m_y+delta_y*2)
                    board.moveChess(human, mach.chesses, mach.m_kings, preChess, aft)
                    board.removeError(win)
            else:
                if status == g.m_chessBoard.Status.PLAIN:
                    aft = Chess(preChess.m_x+delta_x, preChess.m_y+delta_y)
                    board.moveChess(human, mach.chesses, mach.m_kings, preChess, aft)
                else:
                    print ("Invalid move")
        else:
            # machine move
            g.moveAI(mach, human)
        steps += 1

    if human.lost(mach):
        g.m_chessBoard.winText2(win)
    else:
        g.m_chessBoard.winText1(win)

    win.autoflush = False
    g.m_chessBoard.displayBoard(win)
    g.m_chessBoard.displayChess(win)
    g.m_chessBoard.displayButton(win)
    g.m_chessBoard.displayText(win)
    win.autoflush = True
    win.getMouse()
    win.close()

    if train:
        mach.m_model.replay()
        mach.m_model.update_target_model()
        mach.m_model.save(f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Machine Learning Checkers.')
    parser.add_argument('--model', default="model1")
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()
    play(args.model, args.train)
