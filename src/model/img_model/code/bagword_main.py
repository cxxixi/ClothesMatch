#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 00:44:34 2018

@author: renwendi
"""

import os
import os.path as osp
import sklearn.metrics

from bagword_helper import get_bags_of_sifts

data_path = osp.join('..', 'imgdata', 'test')

with open('../../model1/output/output.txt') as f:
    data = f.readlines()

dataset = []

for line in data:
    lineData=line.strip().split(':')
    dataset.append(lineData)
#    dataset.append(lineData[0].split()[0])

a_ids = []

vocab_filename = 'vocab.pkl'

test_num = 100
for idx in range(test_num):
    b_ids = []
    line1 = dataset[idx][0].split()
    a_id = int(line1[0])
    b_ids.append(int(line1[1]))
    linedata1 = dataset[0]
    for i in range(1,len(linedata1)-1):
        b_ids.append(int(linedata1[i].split()[1]))

    a_img_path = str(a_id) + ".jpg"
    ls = os.listdir(data_path)
    for l in ls:
        if l == a_img_path:
            a_full_path = data_path+'/'+a_img_path

    b_full_path = []
    for j in range(200):
        b_id = b_ids[j]

        b_img_path = str(b_id) + ".jpg"

        ls = os.listdir(data_path)
        for l in ls:
            if l == b_img_path:
                temp = data_path+'/'+b_img_path
                b_full_path.append(temp)

    a_image_feats = get_bags_of_sifts([a_full_path], vocab_filename)
    a_image_feats.reshape((1, 200))
    b_image_feats = get_bags_of_sifts(b_full_path, vocab_filename)

    sim_degree = sklearn.metrics.pairwise.cosine_similarity(a_image_feats, b_image_feats)
    print(sim_degree)
    #===save results=========
    outF = open('../output/bag_degree.txt', "a")
    outF.write(str(a_id))
    outF.write("\n")
    for k in range(200):
        outF.write(str(b_ids[k]))
        outF.write(":")
        outF.write(str(round(sim_degree[0][k],4)))
        outF.write(",")
    outF.write("\n")
