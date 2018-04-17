
import numpy as np

class Model:
    def __init__(self):
        self.base_x = np.array([
                [12, 12, 0, 0, 0, 0],
                [12,  0, 12, 0, 0, 12],
                [0,  12, 0, 12, 12, 0],
        ])

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

    def eval(self, x):
        assert(len(x) == len(self.w))
        x = np.array(x)
        r = x.dot(self.w)
        return r.item()

    def update(self, xnew, xold):
        vnew = self.eval(xnew)
        vold = self.eval(xold)
        self.w += self.mu * (vnew - vold) + self.lambd * self.w.sum()


    def calibrate(self):
        delta = np.dot(self.base_x.T, self.base_y - self.base_x.dot(self.w) )
        # regularize
        delta += self.lambd * self.w.sum()
        self.w += (self.mu/self.base_x.shape[0]) * delta
