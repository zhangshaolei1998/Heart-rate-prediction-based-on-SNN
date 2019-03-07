#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import copy
import pandas as pd
import random
import datetime

class Particle(object):
    def __init__(self, dimension):
        self.position = np.random.random([dimension])
        self.v = random.random()
        self.error = float('inf')
        self.best = self.position
    pass

def sigmoid(x):
    return 1 / (1 + np.exp(-x))
    pass

class ParticleSwarmOptimization(object):
    def __init__(self, data, c1 = 0.5, c2 = 0.5, m = 2):
        self.Y = data
        self.dimension = self.Y.shape[1] * 3
        self.iter_max = 1000
        self.pop_size = 1000
        self.c1 = c1
        self.c2 = c2
        self.err_crit = 0.0000001
        self.bestW, self.bestC0, self.bestC1, self.bestError = self.particle_swarm_optimization(m)
        print('bestW:\n', self.bestW)
        print('bestC0:\n', self.bestC0)
        print('bestC1:\n', self.bestC1)
        print('bestError:\n', self.bestError)
        self.saveWC0C1(self.bestW, self.bestC0, self.bestC1)

        self.p = self.get_probability(self.bestW, self.bestC0, self.bestC1, m)
        pass


    def saveWC0C1(self, W, C0, C1, fileName = 'WCoC1.csv'):
        fileName = fileName + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

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
        c0 = position[positionDimension : (2 * positionDimension)]
        c1 = position[(2 * positionDimension) :]
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

    def particle_swarm_optimization(self, m):
        particles = []
        for i in range(self.pop_size):
            particle = Particle(self.dimension)
            particles.append(particle)

        gbest = copy.copy(particles[0])
        err_crit = None
        for i in range(self.iter_max):
            for particle in particles:
                error, p = self.generalized_least_square_error(particle.position, m)
                if error < particle.error:
                    particle.error = error
                    particle.best = particle.position
                if error < gbest.error:
                    err_crit = gbest.error - error
                    gbest = copy.copy(particle)
                particle.v = particle.v + self.c1 * (particle.best - particle.position) \
                             + self.c2 * (gbest.best - particle.position)
                particle.position = particle.position + particle.v

            if err_crit < self.err_crit:
                print('iteration:', i, '\terr_crit:', err_crit, '\terror:', gbest.error)
                break

            if i % 100 == 0:
                print('iteration:', i, '\terr_crit:', err_crit, '\terror:', gbest.error)

        positionDimension = self.Y.shape[1]
        w = gbest.position[: positionDimension]
        c0 = gbest.position[positionDimension: (2 * positionDimension)]
        c1 = gbest.position[(2 * positionDimension):]
        return w, c0, c1, gbest.error
        pass

if __name__ == '__main__':
    ParticleSwarmOptimization()
    pass