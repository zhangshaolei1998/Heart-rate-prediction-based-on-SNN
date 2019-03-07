#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib as mpl
import seaborn as sns

from read_data import read_a_txt

def show_encoder_spike_output(signalFile, spikeTrainFile):
    spikefile = open(spikeTrainFile)
    sigValues = []
    spiValues = []

    sigValues = read_a_txt(signalFile)
    spiValues = list(map(int, spikefile.read()))
    spikefile.close()

    x = range(0,2000)
    plt.subplot(211)
    plt.plot(x, sigValues[0:2000])
    plt.subplot(212)
    plt.plot(x, spiValues[0:2000])
    plt.show()
    pass

def show_neuron_spike_num(dataFile):
    data = pd.read_csv(dataFile, header = None)
    sns.heatmap(data)
    plt.show()
    pass

if __name__ == '__main__':
    show_encoder_spike_output('caijing.a.txt', 'caijing.or.txt')
    # show_neuron_spike_num('spike.txt')
    pass
