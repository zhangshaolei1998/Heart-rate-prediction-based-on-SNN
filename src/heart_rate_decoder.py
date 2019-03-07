#!/usr/bin/python
# -*- coding: utf-8 -*-

import monte_carlo as MC
import particle_swarm_optimization as PSO
import predict_heart_rate as PHR
import numpy as np
import read_actual_heart_rate
import pandas as pd
import accuracy_estimation

def getData(fileName='spike.txt'):
    # return np.random.random([600, 80])
    spikes = pd.read_csv(fileName, header=None).values.T
    return spikes
    pass

def heartRateDecoder():
    print('reading spike data...')
    allSpikeData = getData()
    nSI = allSpikeData.shape[0]
    if not nSI % 600 == 0:
        print('warming: the spikes are not for some complete minute!!!')
        return
    nHI = int(nSI / 600)

    print('getting actual heart rate...')
    labelFileNames = ['caijing.f.txt']
    startTimes = [0]
    stopTimes = [60000]
    actualHeartRates = read_actual_heart_rate.getActualHeartRate(labelFileNames, startTimes, stopTimes)
    # actualHeartRates = [72,72,72,72,72,72,72,72,72,72]
    print('actual heart rate:', actualHeartRates)

    print('caculating heart rate...')
    heartRates = np.zeros([nHI])
    for HI_i in range(nHI):
        print('caculating %d th mins...' % HI_i)
        spikeData = allSpikeData[HI_i * 600 : (HI_i + 1) * 600]

        probability = MC.MonteCarlo(spikeData).p
        # probability = PSO.ParticleSwarmOptimization(spikeData, c1 = 2, c2 = 1, m = 2).p

        heartRate = PHR.PredictHeartRate(probability).heartRate
        heartRate = min(600 - heartRate, heartRate)
        print('HI_i:', HI_i, '\theartRate:', heartRate)
        heartRates[HI_i] = heartRate

    MAPE = accuracy_estimation.meanAveragePercentError(heartRates, actualHeartRates)
    print('Mean Average Percent Error (MAPE):', MAPE)

if __name__ == '__main__':
    heartRateDecoder()

    pass