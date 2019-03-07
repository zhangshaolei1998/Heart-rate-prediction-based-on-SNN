#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def meanAveragePercentError(predictHeartRate, actualHeartRate):
    MAPE = np.mean(np.abs(predictHeartRate - actualHeartRate) / actualHeartRate) * 100
    return MAPE
    pass

if __name__ == '__main__':
    pass