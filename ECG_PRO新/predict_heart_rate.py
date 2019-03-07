#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import math

class PredictHeartRate(object):
    def __init__(self, clusterPr):
        self.clusterPr = clusterPr
        self.ns = clusterPr.shape[0]
        self.maxHeartRate = 100
        self.Pr = np.zeros(self.maxHeartRate)
        self.heartRate = self.predict()
        pass

    def BernoullTrials(self, successCount = 0, totalCount = 0, probability = 1):
        if successCount == self.maxHeartRate:
            self.Pr[successCount - 1] = self.Pr[successCount - 1] + probability * math.pow(self.clusterPr[totalCount, 1], self.ns - totalCount)
        if totalCount == self.ns:
            self.Pr[successCount - 1] = self.Pr[successCount - 1] + probability
            return

        successPr = probability * self.clusterPr[totalCount, 0]
        self.BernoullTrials(successCount + 1, totalCount + 1, successPr)

        failPr = probability * self.clusterPr[totalCount, 1]
        self.BernoullTrials(successCount, totalCount + 1, failPr)
        pass

    def hard_assignments(self):
        return np.sum(np.argmax(self.clusterPr, axis = 1))
        pass

    def predict(self):
        # self.BernoullTrials()
        # heartRate = np.sum(self.Pr * (np.arange(self.ns) + 1))

        heartRate = self.hard_assignments()
        return heartRate
        pass

if __name__ == '__main__':
    PredictHeartRate(np.random.random([600, 2]))
    pass