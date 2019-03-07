#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

def read_annotation(fileName):
    annotations = []
    with open(fileName) as file:
        file.readline()
        for line in file:
            line_list = line.split()
            annotations.append(float(line_list[0]) * 250)
    pass

def read_signal(fileName):
    pass

def svdb_to_standard(svdbName, tarFileName):
    annotationFileName = svdbName + '_a.txt'
    signalFileName = svdbName + '_s.csv'

    tarAFileName = tarFileName + '.a.txt'
    tarFFileName = tarFileName + '.f.txt'


    pass

if __name__ == '__main__':
    pass