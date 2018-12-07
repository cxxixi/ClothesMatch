#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:31:13 2018

@author: renwendi
"""
import numpy as np
import cv2
import os.path as osp
from glob import glob
from random import shuffle
import cyvlfeat as vlfeat
import pickle

data_path = osp.join('..', 'data')
categories = ['tianchi_fm_img2_1.', 'tianchi_fm_img2_2','tianchi_fm_img2_3','tianchi_fm_img2_4']

def get_image_paths(data_path, categories):
    all_image_paths = []
    test_image_paths = []
    fmt='jpg'
    #train
    for cat in categories:
        pth = osp.join(data_path, 'train', cat, '*.{:s}'.format(fmt))
        pth = glob(pth)
        shuffle(pth)
        all_image_paths.extend(pth)
    #test
    pth = osp.join(data_path, 'test', '*.{:s}'.format(fmt))
    pth = glob(pth)
    shuffle(pth)
    test_image_paths.extend(pth)
    return all_image_paths, test_image_paths

all_image_paths, test_image_paths = get_image_paths(data_path, categories)

def im2single(im):
  im = im.astype(np.float32) / 255
  return im

def load_image(path):
  return im2single(cv2.imread(path))[:, :, ::-1]

def load_image_gray(path):
  img = load_image(path)
  return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def build_vocabulary(image_paths, vocab_size):
  dim = 128      # length of the SIFT descriptors that you are going to compute.
  vocab = np.zeros((vocab_size,dim))

  num = len(image_paths)
  sift = np.zeros([num*20, 128])
  for i in range(num):
      img = load_image_gray(image_paths[i])
      img = np.float32(img)
      frames, sift_features = vlfeat.sift.dsift(img, fast=True, step=10)
      num_fea = len(sift_features)
      select_fea_num = np.random.permutation(num_fea)
      select_sift = sift_features[select_fea_num[0:20],:]
      sift[i*20:(i+1)*20,:] = select_sift

  vocab = vlfeat.kmeans.kmeans(sift, vocab_size)
  return vocab

vocab_filename = 'vocab.pkl'
if not osp.isfile(vocab_filename):
    # Construct the vocabulary
    print('No existing visual word vocabulary found. Computing one from training images')
    vocab_size = 200  # Larger values will work better (to a point) but be slower to compute
    vocab = build_vocabulary(all_image_paths, vocab_size)
    with open(vocab_filename, 'wb') as f:
        pickle.dump(vocab, f)
        print('{:s} saved'.format(vocab_filename))

def get_bags_of_sifts(image_paths, vocab_filename):
  """Returns:
     image_feats: N x d matrix, where d is the dimensionality of the
          feature histogram representation. Here, d is vocab_size).
          N is number of test images.
  """
  with open(vocab_filename, 'rb') as f:
    vocab = pickle.load(f)

  vocab_size = 200
  num = len(image_paths)
  res = np.zeros([num, vocab_size])

  my_bins = np.zeros(vocab_size+1)
  for i in range(vocab_size+1):
      my_bins[i] = i

  for i in range(num):
      img = load_image_gray(image_paths[i])
      img = np.float32(img)
      frames, sift_feats = vlfeat.sift.dsift(img, fast=True, step=3)
      sift_feats = np.float64(sift_feats)
      assignments = vlfeat.kmeans.kmeans_quantize(sift_feats, vocab)
      hist_sift, bin_edges = np.histogram(assignments, bins=my_bins)
      hist_sift_norm=np.linalg.norm(hist_sift)
      hist = hist_sift / hist_sift_norm
      res[i, :] = hist

  return res

#test_image_feats = get_bags_of_sifts(test_image_paths, vocab_filename)
