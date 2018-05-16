"""
Train AI players

Takes the following parameters:

    --model: the file to store the learned model to disk.

            Given a value of <file>, this program produce the
            files: <file>1.h5, stores the weights first agent
                   <file>1.epsilon.p, stores the exploration rate

                   <file>2.h5 and <file>2.epsilon.p store the same
                   info for the second agent.

                   <file>.csv stores the win-loss record of the agent.
                   Each row correspond to a played game.
                   The first column is a 1 if the agent1 was the winner,
                   and 0 is the agent2 was the winner. The second column
                   is the number of moves played in that game.

            These files are stored in the save directory.

    --episodes: The number of games to play
"""


from checkers import *
import numpy as np
import random
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
    def reset(self):
        self.m_chessBoard.reset()
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

        if done:
            if player.lost(opp):
                reward = -12
            elif opp.lost(player):
                reward = 12
            else:
                reward = -2

        player.m_model.remember(state, reward, next_state, done)

def train(f, episodes):
    g = Game()
    f1 = './save/{}1'.format(f)
    f2 = './save/{}2'.format(f)
    g.model1.load(f1)
    g.model2.load(f2)

    # use 3 rounds of lookahead minimax
    g.setMaxSteps(3)

    for e in range(episodes):
        print(g.model1.epsilon)
        g.reset()
        steps = 0

        # play a game
        while not g.end():
            g.printChessTable()
            g.printPlayerChess()
            g.printAIChess()
            if  steps % 2 == 0:
                g.moveAI(g.player1, g.player2)
            else:
                g.moveAI(g.player2, g.player1)
            steps += 1

        print("steps", steps)

        with open('./save/{}.csv'.format(f), 'a+') as fo:
            win = 1 if g.player2.lost(g.player1) else 0
            fo.write('{},{}\n'.format(win, steps))

        g.model1.update_target_model()
        g.model2.update_target_model()

        # learn from the game
        # apply learning algo
        g.model1.replay()
        g.model2.replay()

        if e % 10 == 0:
            g.model1.save(f1)
            g.model2.save(f2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default="model")
    parser.add_argument('--episodes', default=1001, type=int)
    args = parser.parse_args()
    train(args.file, args.episodes)
