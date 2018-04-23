
import numpy as np

class Model:
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
        self.base_x = np.array([
                [12, 12, 0, 0, 0, 0],
                [12,  0, 12, 0, 0, 12],
                [0,  12, 0, 12, 12, 0],
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

        self.m = 6  # number of features
        self.w = np.zeros((self.m,1))
        self.mu = 0.1
        self.lambd = 0.001

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
