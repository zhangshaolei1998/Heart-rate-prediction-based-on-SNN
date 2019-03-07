#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import datetime

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    pass

class MonteCarlo(object):
    def __init__(self, data):
        self.Y = data
        self.dimension = self.Y.shape[1] * 3
        self.n = 1000000
        self.bestW, self.bestC0, self.bestC1, self.bestError = self.monte_carlo()
        print('bestW:\n', self.bestW)
        print('bestC0:\n', self.bestC0)
        print('bestC1:\n', self.bestC1)
        print('bestError:\n', self.bestError)
        self.saveWC0C1(self.bestW, self.bestC0, self.bestC1)

        self.p = self.get_probability(self.bestW, self.bestC0, self.bestC1)
        pass

    def saveWC0C1(self, W, C0, C1, fileName = 'WCoC1'):
        fileName = fileName + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
        print('saving', fileName, '...')

        positionDimension = self.Y.shape[1]
        W = np.reshape(W, [1, positionDimension])
        C0 = np.reshape(C0, [1, positionDimension])
        C1 = np.reshape(C1, [1, positionDimension])

        data = np.append(W, C0, axis = 0)
        data = np.append(data, C1, axis = 0)

        dataFrame = pd.DataFrame(data)
        dataFrame.to_csv(fileName, header = None)
        pass

    def generalized_least_square_error(self, position, m = 2):
        positionDimension = self.Y.shape[1]
        w = position[: positionDimension]
        c0 = position[positionDimension: (2 * positionDimension)]
        c1 = position[(2 * positionDimension):]
        size = self.Y.shape[0]

        Y = self.Y * sigmoid(w - 0.5) / 100

        d0_2 = np.sum(((Y - c0) ** 2), axis=1).reshape(size, 1)
        d1_2 = np.sum(((Y - c1) ** 2), axis=1).reshape(size, 1)

        p_i0 = 1 / (1 + np.power((d0_2 / d1_2), 1 / (m - 1)))
        p_i1 = 1 / (1 + np.power((d1_2 / d0_2), 1 / (m - 1)))
        p = np.append(p_i0, p_i1, axis=1)

        d0_2 = np.power(p_i0, m) * d0_2
        d1_2 = np.power(p_i1, m) * d1_2
        error = np.sum((d0_2 + d1_2))
        return [error, p]
        pass

    def get_probability(self, w, c0, c1, m = 2):
        size = self.Y.shape[0]
        Y = self.Y * sigmoid(w - 0.5) / 100

        d0_2 = np.sum(((Y - c0) ** 2), axis=1).reshape(size, 1)
        d1_2 = np.sum(((Y - c1) ** 2), axis=1).reshape(size, 1)

        p_i0 = 1 / (1 + np.power((d0_2 / d1_2), 1 / (m - 1)))
        p_i1 = 1 / (1 + np.power((d1_2 / d0_2), 1 / (m - 1)))
        p = np.append(p_i0, p_i1, axis=1)
        return p
        pass

    def monte_carlo(self):
        best_error = float('inf')
        best_position = None
        for i in range(self.n):
            position = np.random.random([self.dimension])
            error, p = self.generalized_least_square_error(position)
            if error < best_error:
                best_error = error
                best_position = position

            if i % 10000 == 0:
                print('iteration:', i, '\terror:', best_error, '\tbest_position for pre six:', best_position[:6])

        positionDimension = self.Y.shape[1]
        w = best_position[: positionDimension]
        c0 = best_position[positionDimension: (2 * positionDimension)]
        c1 = best_position[(2 * positionDimension):]
        return w, c0, c1, best_error
        pass

if __name__ == '__main__':
    MonteCarlo()
    pass