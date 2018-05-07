# -*- coding: utf-8 -*-
import random
import numpy as np
import pickle
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
        self.memory_end = deque(maxlen=2000)

        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001

        self.model_end = self._build_model()
        self.model_reg = self._build_model()
        self.model = self._build_model()

        self.target_model_end  =self._build_model()
        self.target_model_reg  = self._build_model()
        self.update_target_model()

    def _huber_loss(self, target, prediction):
        # sqrt(1+error^2)-1
        error = prediction - target
        return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.m, activation='tanh'))
        model.add(Dense(24, activation='tanh'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss=self._huber_loss,
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model_reg.set_weights(self.model_reg.get_weights())
        self.target_model_end.set_weights(self.model_end.get_weights())

    def endgame(self, state):
        return (state[0] + state[1]) < 5 or (state[6] + state[7]) < 5

    def remember(self, state, reward, next_state, done):
        s = state
        state = np.array(state).reshape(1, self.m)
        next_state = np.array(next_state).reshape(1, self.m)

        if self.endgame(s):
            self.memory_end.append((state, reward, next_state, done))
        else:
            self.memory.append((state, reward, next_state, done))

    def eval(self, state):
        assert(len(state) == self.m)
        s = state
        state = np.array(state).reshape(1, self.m)

        if self.endgame(s):
            return self.model_end.predict(state).item()
        else:
            return self.model_reg.predict(state).item()

    def replay(self):
        self.replay_model(self.memory, self.model_reg, self.target_model_reg)
        self.replay_model(self.memory_end, self.model_end, self.target_model_end)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def replay_model(self, memory, model, target_model):
        batch_size = min(len(memory), 256)
        minibatch = random.sample(memory, batch_size)
        for state,reward, next_state, done in minibatch:
            target = model.predict(state).item()
            if done:
                target = reward
            else:
                t = target_model.predict(next_state).item()
                target = reward + self.gamma * np.amax(t)
            target = np.array([target])
            model.fit(state, target, epochs=1, verbose=0)

    def load(self, name):
        self.model_reg.load_weights(name + '.h5')
        self.model_end.load_weights(name + '.end.h5')
        with open(name + '.epsilon.p', 'rb') as f:
            self.epsilon = pickle.load(f)

    def save(self, name):
        self.model_reg.save_weights(name + '.h5')
        self.model_end.save_weights(name + '.end.h5')
        with open(name + '.epsilon.p', 'wb') as f:
            pickle.dump(self.epsilon, f)
