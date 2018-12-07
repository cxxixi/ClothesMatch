#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 01:54:27 2018

@author: renwendi
"""

from matplotlib import pyplot as plt
import numpy as np
import cv2
import os.path as osp
import os
import sklearn.metrics

def color_histogram_feature(image_paths):
    num = len(image_paths)
    res = np.zeros([num, 256*3])

    for i in range(num):

        image = cv2.imread(image_paths[i])

        #remove background color
#        mask = np.zeros(image.shape[:2],np.uint8)
#
#        bgdModel = np.zeros((1,65),np.float64)
#        fgdModel = np.zeros((1,65),np.float64)
#
#        rect = (50,50,450,290)
#        cv2.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
#
#        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
#        image = image*mask2[:,:,np.newaxis]

        chans = cv2.split(image)
        colors = ("b", "g", "r")
        color_features = np.zeros(256*3)

        # loop over the image channels
        index = 0
        for (chan, color) in zip(chans, colors):
            hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
            color_features[256*index:256*(index+1)] = hist.flatten()
            index += 1

        res[i, :] = color_features

    return res

data_path = osp.join('..', 'imgdata', 'test')

with open('../../model1/output/output.txt') as f:
    data = f.readlines()

dataset = []

for line in data:
    lineData=line.strip().split(':')
    dataset.append(lineData)
#    dataset.append(lineData[0].split()[0])

a_ids = []

test_num = 100
num_200 = 200

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

    a_image_feats = color_histogram_feature([a_full_path])
    a_image_feats.reshape((1, 256*3))
    b_image_feats = color_histogram_feature(b_full_path)

    sim_degree = sklearn.metrics.pairwise.cosine_similarity(a_image_feats, b_image_feats)
    #print(a_id)
    #===save results=========
    outF = open('../output/color_degree_256.txt', "a")
    outF.write(str(a_id))
    outF.write("\n")
    for k in range(200):
        outF.write(str(b_ids[k]))
        outF.write(":")
        outF.write(str(round(sim_degree[0][k],4)))
        outF.write(",")
    outF.write("\n")
