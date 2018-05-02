
import numpy as np
import time
import pickle
import os

class LearningModel:
    def __init__(self):
        '''
        The baseline examples.
        Each row is a feature vector of 6 features:
        1. number of own pieces
        2. number of opponent pieces
        3. number of own kings
        4. number of opponent kings
        5. number of own pieces threatened
        6. number of oppoenents pieces threatened
        '''

        '''
        These examples correspond to:
        initial board,
        winning,
        losing
        '''
        self.board_init = np.array(
                [12, 0, 3, 4, 6, 0, 12, 0, 3, 4, 6, 0]
                )

        self.base_x = np.array([
                self.board_init,
                [12, 12, 12, 12, 0, 12, 0, 0, 0, 0, 7, 0],
                [0, 0, 0, 0, 7, 0, 12, 12, 12, 12, 0, 12],
        ])

        '''
        initial board has score 0
        winning has score 1000
        losing has score -1000
        '''
        self.base_y = np.array([
            [    0],
            [ 1000],
            [-1000],
        ])

        self.m = 12  # number of features
        self.w = np.zeros((self.m,1))
        self.mu = 0.1
        self.lambd = 0.001
        self.moves = np.array(self.board_init)

        for i in range(int(1e3*self.lambd)):
            self.calibrate()

    # method used to evaluate a board as
    # categorized by feature vector x
    def eval(self, x):
        assert(len(x) == len(self.w))
        x = np.array(x)
        r = x.dot(self.w)
        return r.item()

    # update the weights by evaluating the
    # difference between the scores of vectors
    # xold and xnew
    def update(self, xnew, xold):
        vnew = self.eval(xnew)
        vold = self.eval(xold)
        self.w += self.mu * (vnew - vold) * xold + self.lambd * self.w.sum()


    # calibrate the feature examples toward the baseline examples
    def calibrate(self):
        delta = np.dot(self.base_x.T, self.base_y - self.base_x.dot(self.w) )
        # regularize
        delta += self.lambd * self.w.sum()
        self.w += (self.mu/self.base_x.shape[0]) * delta

    def reload_model(self):
        try:
            with open("w.pl", "rb") as f:
                self.w = pickle.load(f)
        except:
            print("cant reload model, using default")

    def mutate(self, model):
        assert(len(model.w) == len(self.w))

        idx = np.random.randint(self.m, size=self.m//3)

        for i in range(self.m):
            if i in idx:
                r = np.random.uniform(low=1/3, high=3)
                self.w[i] = r * model.w[i]
            else:
                self.w[i] = model.w[i]

    def logmove(self, x):
        x = np.array(x)
        self.moves = np.vstack((self.moves, x))

    def analyze_result(self):

        last_play = self.moves[-1]
        if last_play[0] == 0:
            won = False
            score_last = -1000
        elif last_play[6] == 0:
            won = True
            score_last = 1000
        else:
            raise Exception("Neither Player has Lost")

        print("init w:", self.w)

        n_moves = self.moves.shape[0]
        n_times = 2500

        for _ in range(n_times):
            self.w += self.mu * (score_last - self.eval(last_play)) * last_play
            for i in range(n_moves-2, -1, -1):
                curr = self.moves[i]
                succ = self.moves[i+1]
                self.w += self.mu * (self.eval(succ) - self.eval(curr)) * curr
            self.w += self.mu * (0 - self.eval(self.moves[0])) * self.moves[0]
            for i in range(0, n_moves-1, 1):
                curr = self.moves[i]
                succ = self.moves[i+1]
                self.w += self.mu * (self.eval(succ) - self.eval(curr)) * curr

        with open("w.pl", "wb") as f:
            pickle.dump(self.w, f)
