#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 21:27:08 2018

@author: renwendi
"""
from util2 import *


if __name__ == "__main__":

    with open('../model1/output/output.txt') as f:
        data = f.readlines()
    dataset = []

    for line in data:
        lineData=line.strip().split(':')
        dataset.append(lineData)

    Model2_Res = []
    test_num = 100
    for idx in range(test_num):

        line1 = dataset[idx][0].split()
        a_id = int(line1[0])
        b_ids = []
        b_ids.append(int(line1[1]))
        linedata1 = dataset[0]

        for i in range(1,len(linedata1)-1):
            b_ids.append(linedata1[i].split()[1])

        res = match_degree_200(a_id, b_ids)
        # print(res)
        Model2_Res.append(res)

        outF = open('./output/model2_degree2.txt', "a")
        outF.write(str(a_id))
        outF.write("\n")
        for k in range(200):
            outF.write(str(res[0][k]))
            outF.write(":")
            outF.write(str(res[1][k]))
            outF.write(",")
        outF.write("\n")
