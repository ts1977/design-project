
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

        [score, chessPrev, chessAft] = self.m_chessBoard.oneStep(player.m_model, player, opp, 1)
        print("score = ", score)

        print ("moving {} to {}".format(chessPrev, chessAft))
        self.m_chessBoard.moveChess(player, opp.chesses, opp.m_kings, chessPrev, chessAft)

        next_state = self.board.getBoardData(player, opp)

        reward = len(player)-len(opp)
        done = self.end()
        player.m_model.remember(state, reward, next_state, done)

TURNS = 5

# stage a match between two models
# winner is decided by best of 5
def match(m1, m2):
    g = Game()
    g.setMaxSteps(3)

    g.player1.m_model = m1
    g.player2.m_model = m2

    wins1 = 0
    wins2 = 0

    for e in range(TURNS):
        g.reset()
        steps = 0

        while not g.end():
            if  steps % 2 == 0:
                g.moveAI(g.player1, g.player2)
            else:
                g.moveAI(g.player2, g.player1)
            steps += 1

        g.model1.update_target_model()
        g.model2.update_target_model()

        g.model1.replay()
        g.model2.replay()

        if g.player1.lost(g.player2):
            wins2 += 1
        if g.player2.lost(g.player1):
            wins1 += 1

        if len(g.player1) > len(g.player2):
            wins1 += 1
        else:
            wins2 += 1

        if wins1 > (TURNS//2):
            return m1
        if wins2 > (TURNS//2):
            return m2

    return m1 if wins1 > TURNS//2 else m2

# play a tournament round with 8 contestants
def tournament_round(models):
    random.shuffle(models)

    while len(models) > 1:
        print("playing match...", end="")
        m1 = models.pop(0)
        m2 = models.pop(0)
        winner = match(m1, m2)
        print("done")
        models.append(winner)

    return models[0]

def evolution(winner):
    models = [winner]

    for _ in range(3):
        m = LearningModel()
        m.mutate(winner)
        models.append(m)

    return models + [LearningModel() for _ in range(4)]

def tournament(f, rounds):
    winner = LearningModel()
    winner.load('./save/{}'.format(f))
    models = [LearningModel() for _ in range(8)]
    models[0] = winner

    for r in range(rounds):
        print("Playing round {}".format(r))
        winner = tournament_round(models)
        winner.save('./save/{}'.format(f))
        models = evolution(winner)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default="t1")
    parser.add_argument('--rounds', default=1000, type=int)
    args = parser.parse_args()

    tournament(args.file, args.rounds)
