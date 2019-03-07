#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def read_a_txt(fileName):
    values = []
    file = open(fileName)
    for value in file:
        values.append(float(value))
    file.close()
    return values

def read_f_txt(filename):
    values = pd.read_csv(filename, header=None)
    return values.values[:,0]

if __name__ == '__main__':
    values = read_a_txt('caijing.a.txt')
    print('max:',max(values))
    print('min:',min(values))
    total = sum(values)
    num = len(values)
    avg = total/num
    print('sum:',total)
    print('num:',num)
    print('avg:',avg)
    sdsq = sum([(i - avg) ** 2 for i in values])
    stdev = (sdsq / (num)) ** .5
    print('std:',stdev)
