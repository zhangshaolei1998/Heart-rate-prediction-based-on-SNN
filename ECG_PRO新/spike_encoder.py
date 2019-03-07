#!/usr/bin/python
# -*- coding: utf-8 -*-

from read_data import read_a_txt

def spike_encoder(inputFile, outputFile, positionFile, delta = 20):
    result = []
    positions = []
    values = read_a_txt(inputFile)

    print('encoding ...')
    for i, value in enumerate(values):
        if i == 0:
            print(value)
            result.append(0)
            Uthr = value + delta / 2
            Lthr = value - delta / 2
        else:
            if value >= Uthr:
                result.append(1)
                positions.append(i)
                while value >= Uthr:
                    Lthr = Uthr
                    Uthr = Uthr + delta
            elif value < Lthr:
                result.append(0)
                while value < Lthr:
                    Uthr = Lthr
                    Lthr = Lthr - delta
            else:
                result.append(0)

    print('output to outputFile')
    with open(outputFile,'w') as file:
        for value in result:
            file.write(str(value))
    print('output to positionFile')
    with open(positionFile, 'w') as file:
        for p in positions:
            file.write(str(p) + '\n')

    return result, positions
    pass

def spike_encoder_rela(inputFile, outputFile, positionFile, delta = 2):
    result = [0]
    positions = []
    values = read_a_txt(inputFile)
    print('encoding ...')
    for i in range(len(values) - 1):
        if values[i + 1] - values[i] >= delta:
            result.append(1)
            positions.append((i + 1) * 4)
        else:
            result.append(0)

    print('output to outputFile')
    with open(outputFile, 'w') as file:
        for value in result:
            file.write(str(value))
    print('output to positionFile')
    with open(positionFile, 'w') as file:
        for p in positions:
            file.write(str(p) + '\n')

    return result, positions

if __name__ == '__main__':
    # spike_encoder('caijing.a.txt', 'caijing.ot.txt', 'caijing.op.txt')
    spike_encoder_rela('caijing.a.txt', 'caijing.or.txt', 'caijing.op.txt')
    pass