#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def getActualHeartRate(fileNames = ['caijing.f.txt'], startTimes = [0], stopTimes = [60000]):
    heartRates = []
    for i in range(len(fileNames)):
        label = pd.read_csv(fileNames[i], header=None)
        label = label.values[:, 0] * 4
        nHI = int((stopTimes[i] - startTimes[i]) / 60000)

        for j in range(nHI):
            label = label[label >= (startTimes[i] + j * 60000)]
            label = label[label < (startTimes[i] + (j + 1) * 60000)]
            heartRate = label.shape[0]
            heartRates.append(heartRate)

    return np.array(heartRates)
    pass

if __name__ ==  '__main__':
    fileNames = ['caijing.f.txt']
    startTime = [0]
    stopTime = [60000]
    heartRates = getActualHeartRate(fileNames, startTime, stopTime)
    print(heartRates)
    pass