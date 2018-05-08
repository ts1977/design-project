
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

        if random.random() < player.m_model.epsilon:
            moves = list(self.m_chessBoard.possible_moves(player, opp))
            [(_, chessPrev, chessAft)] = random.sample(moves, 1)
        else:
            [score, chessPrev, chessAft] = self.m_chessBoard.oneStep(player.m_model, player, opp, 1)
            print("score = ", score)

        print ("moving" + str(chessPrev) + ", to" + str(chessAft))
        self.m_chessBoard.moveChess(player, opp.chesses, opp.m_kings, chessPrev, chessAft)

        next_state = self.board.getBoardData(player, opp)

        reward = len(player)-len(opp)
        done = self.end()
        player.m_model.remember(state, len(player)-len(opp), next_state, done)

def play(second, model, train):
    g = Game()
    board = g.m_chessBoard
    g.setMaxSteps(3)
    chess = Chess()
    win = GraphWin('Checkers', 1000, 1000)
    steps = 0

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
            [delta_x, delta_y] = board.chessDirection(preChess, aftChess)

            if (delta_x == 0 or
                not board.isValid(aftChess.m_x, aftChess.m_y) or
                abs(aftChess.m_y - preChess.m_y)> 2 or
                (aftChess.m_x - preChess.m_x) > 2):
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
    parser.add_argument('--second', action='store_true')
    parser.add_argument('--model', default="model1")
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()
    play(args.second, args.model, args.train)
