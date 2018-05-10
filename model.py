# -*- coding: utf-8 -*-
import random
import numpy as np
import pickle
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

class LearningModel:
    def __init__(self):
        self.m = 10

        self.memory = deque(maxlen=2000)

        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001

        self.model = self._build_model()
        self.target_model =self._build_model()
        self.update_target_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.m, activation='tanh'))
        model.add(Dense(24, activation='tanh'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, reward, next_state, done):
        state = np.array(state).reshape(1, self.m)
        next_state = np.array(next_state).reshape(1, self.m)
        self.memory.append((state, reward, next_state, done))

    def eval(self, state):
        assert(len(state) == self.m)
        state = np.array(state).reshape(1, self.m)
        return self.model.predict(state).item()

    def replay(self):
        batch_size = min(len(self.memory), 256)
        minibatch = random.sample(self.memory, batch_size)

        for state,reward, next_state, done in minibatch:
            target = self.model.predict(state).item()
            if done:
                target = reward
            else:
                t = self.target_model.predict(next_state).item()
                target = reward + self.gamma * np.amax(t)
            target = np.array([target])
            self.model.fit(state, target, epochs=1, verbose=0)

        self.epsilon = max(self.epsilon*self.epsilon_decay,
                    self.epsilon_min)


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
