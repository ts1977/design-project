# -*- coding: utf-8 -*-
import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

import pdb

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
        self.target_model = self._build_model()
        self.update_target_model()

    def _huber_loss(self, target, prediction):
        # sqrt(1+error^2)-1
        error = prediction - target
        return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.m, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss=self._huber_loss,
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
        batch_size = min(len(self.memory), 128)
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

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

