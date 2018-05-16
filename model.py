
import random
import numpy as np
import pickle
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

# Code was modified from:
# https://keon.io/deep-q-learning/

class LearningModel:
    def __init__(self):
        # the number of features
        self.m = 10

        self.memory = deque(maxlen=2000)

        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0   # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001

        self.model = self._build_model()
        self.target_model =self._build_model()
        self.update_target_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model

        # Has 10 inputs, 2 hidden layers of 24 neurons
        # and 1 linear output. Uses tanh activation

        model = Sequential()
        model.add(Dense(24, input_dim=self.m, activation='tanh'))
        model.add(Dense(24, activation='tanh'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    # log a move
    def remember(self, state, reward, next_state, done):
        state = np.array(state).reshape(1, self.m)
        next_state = np.array(next_state).reshape(1, self.m)
        self.memory.append((state, reward, next_state, done))

    # evaluate a state
    def eval(self, state):
        assert(len(state) == self.m)
        state = np.array(state).reshape(1, self.m)
        return self.model.predict(state).item()

    def mutate(self, other):
        self.model.set_weights(other.model.get_weights())
        self.weights_mutate(self.model.get_weights())
        self.update_target_model()

    def weights_mutate(self, weights):
        for x in range(0, len(weights), 2):
            for y in range(len(weights[x])):
                for z in range(len(weights[x][y])):
                    if np.random.uniform(0, 1) < 0.20:
                        diff = random.uniform(-0.5,0.5)
                        weights[x][y][z] += diff

    # learn from the game results
    def replay(self):
        batch_size = min(len(self.memory), 256)
        minibatch = random.sample(self.memory, batch_size)

        for state,reward, next_state, done in minibatch:
            target = self.model.predict(state).item()
            if done:
                # target for last move is just the reward
                target = reward
            else:
                # target is the reward, plus the reward expected
                # in the next_state
                t = self.target_model.predict(next_state).item()
                target = reward + self.gamma * np.amax(t)
            target = np.array([target])
            # do one epoch of backpropogation
            self.model.fit(state, target, epochs=1, verbose=0)

        # decay the exploration rate
        self.epsilon = max(self.epsilon*self.epsilon_decay,
                    self.epsilon_min)


    # load and save model files

    def load(self, name):
        print('loading model {}...'.format(name), end='')
        try:
            self.model.load_weights(name + '.h5')
            with open(name + '.epsilon.p', 'rb') as f:
                self.epsilon = pickle.load(f)
            print('done')
        except:
            print('failed')

    def save(self, name):
        self.model.save_weights(name + '.h5')
        with open(name + '.epsilon.p', 'wb') as f:
            pickle.dump(self.epsilon, f)
