#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import scipy.interpolate as itp
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import shutil


def decompileDataPI(file_list, output_dir):  # 反编译数据

    file_list_input = open(file_list, 'r')  # 读取holter数据文件名

    while True:
        line = file_list_input.readline()
        if not line: break

        file_in = open(line[:-1], 'rb')  # 以2进制方式打开.a或.ar文件
        fileTemp = os.path.basename(line)[:-1]

        if line[:-1].endswith('.ar'):
            count = 0
            r_peak = 0
            file_out = open(output_dir + fileTemp + ".txt", 'a+')

            while True:
                byte = file_in.read(1)  # 读取一个字节
                if not byte: break
                count += 1

                if count <= 4:
                    r_peak += ord(byte) * (256 ** (count - 1)) * 2  # resampled to 250Hz

                    if count == 4:
                        file_out.write(str(r_peak) + ',')  # 写入文件中
                        r_peak = 0

                elif count == 7:
                    count %= 7
                    file_out.write(str(ord(byte)) + '\n')  # 写入文件中

                else:
                    file_out.write(str(ord(byte)) + ',')  # 写入文件中

            file_in.close()
            file_out.close()

        elif line[:-1].endswith('.a'):
            ecg_data = []
            while True:
                byte = file_in.read(1)  # 读取一个字节
                if not byte: break
                ecg_data.append(ord(byte))

            file_in.close()
            resampled_ecg_data = interpolationData(ecg_data)  # resampled to 250Hz

            np.savetxt(output_dir + fileTemp + ".txt", resampled_ecg_data)

    file_list_input.close()


def interpolationData(data):
    axis_x = np.arange(0, len(data), 1)  # 创建x等差序列
    axis_xInterpolate = np.arange(0, len(data), 0.5)  # 创建x插值后的等差序列

    tck = itp.splrep(axis_x, data, s=0, k=3)
    yInterpolate = itp.splev(axis_xInterpolate, tck, der=0)

    return yInterpolate


def ListFiles(input_dir, output_file, ends_1, ends_2):  # 将需要反编译的文件写入文本文档
    files_in = os.listdir(input_dir)
    output = open(output_file, 'a+')
    for name in files_in:
        fullname = os.path.join(input_dir, name)
        if (os.path.isdir(fullname)):  # os.path.isdir()函数判断某一路径是否为目录
            ListFiles(fullname, output_file, ends_1, ends_2)

        elif (fullname.endswith(ends_1) | fullname.endswith(ends_2)):
            output.write(fullname + '\n')  # 将文件全路径写入文件中

    output.close()

input_dir = 'E:/holter_output/Holter5/'     #Holter0-4
output_dir = 'E:/holter_output/holter_vadidate/'

ends_1 = ".a"
ends_2 = ".ar"
file_list = output_dir + "file_list.txt"        #Holter0-4

ListFiles(input_dir, file_list, ends_1, ends_2)

decompileDataPI(file_list, output_dir)