#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: hzhu rren
"""
import math
import sys
sys.path.append('../../')

from db import DB_Object

def shareItem(item_1, item_2):
    total = 0
    for k in item_1:
        if k in item_2 and item_1[k] == item_2[k]:
            total = total + item_1[k]
    return total

def match_degree_200(a_id, sub1_200_list):
    db = DB_Object("../../Clothes.sqlite")
    test = db.fetch_data(num=6)
    item_ids=[]
    for i in range(len(test)):
        item_ids.append(test[i][0])

    item_ids_set = list(set(item_ids))
    #a_id=1417 (test)
    bought_history1 = db.fetch_data(num=5, item_id=a_id)

    res = [[],[]]
    for b_id in sub1_200_list:
    #for b_id in item_ids_set[:200]:
        item_1 = {}
        item_2 = {}
        bought_history2 = db.fetch_data(num=5,item_id=b_id)
        for i in range(len(bought_history1)):
            customer_all1 = bought_history1[i]
            c1_id = customer_all1[0]
            b1_id = customer_all1[1]
            date1 = customer_all1[2]
            if str(c1_id)+str(date1) in item_1:
                item_1[str(c1_id)+str(date1)] += 1
            else:
                item_1[str(c1_id)+str(date1)] = 1

        for i in range(len(bought_history2)):
            customer_all2 = bought_history2[i]
            c2_id = customer_all2[0]
            b2_id = customer_all2[1]
            date2 = customer_all2[2]
            if str(c2_id)+str(date2) in item_2:
                item_2[str(c2_id)+str(date2)] += 1
            else:
                item_2[str(c2_id)+str(date2)] = 1

        match_degree = shareItem(item_1,item_2)
        res[0].append(b_id)
        res[1].append(match_degree)
    return res
