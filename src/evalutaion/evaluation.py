#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 10:52:14 2018

@author: renwendi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 22:40:35 2018

@author: renwendi
"""
import sys
sys.path.append('../')

from db import DB_Object
import numpy as np

def ap(pred_list, true_list):
    return ap

def one_ap(b_ids):
    #map 200
    sumk = 0
    sumap = 0
    for k in range(20):
        for item in match_list:
            if(int(b_ids[k]) == int(item)):
                deltak = 1
                sumk += 1
                break
            deltak = 0
        pk = sumk / (k + 1)
        temp = deltak / (1 - np.log(pk))
        sumap += temp
    one_ap = sumap / len(match_list)
#    print(one_ap, idx, a_id)

    return one_ap

if __name__ == "__main__":

#====================read model1====================
        with open('./output/model1_degree.txt') as f:
                data = f.readlines()

        dataset = []

        for line in data:
            lineData=line.strip().split(':')
            dataset.append(lineData)
        #    dataset.append(lineData[0].split()[0]

        #====================read cv1====================
        with open('./output/bag_degree.txt') as f:
                data = f.readlines()

        dataset_bag = []

        for line in data:
            lineData=line.strip().split(':')
            dataset_bag.append(lineData)

        #====================read cv2====================
        with open('./output/color_degree_256.txt') as f:
                data = f.readlines()

        dataset_color = []

        for line in data:
            lineData=line.strip().split(':')
            dataset_color.append(lineData)
        #===============================================

        num_test = 100
        m_ap_model1 = 0
        m_ap_bag = 0
        m_ap_model1_bag = 0
        m_ap_color = 0
        for idx in range(num_test):

            #================model1 degree================

            line1 = dataset[idx][0].split()

            a_id = int(line1[0])
            b_ids = []
            degrees_model1 = []

            b_ids.append(int(line1[1]))


            linedata1 = dataset[0]

            for i in range(1,len(linedata1)-1):
                b_ids.append(int(linedata1[i].split()[1]))
                degrees_model1.append(float(linedata1[i].split()[0]))

            line_last = dataset[idx][len(linedata1)-1].split()
            degrees_model1.append(float(line_last[0]))

            #================model1 end================
            #================cv 1=====================
            degrees_bag = []
            linedata = dataset_bag[idx*2+1]
            for i in range(1, len(linedata)):
                degrees_bag.append(float(linedata[i].split(",")[0]))

            bag_table = np.zeros([200,2])
            for i in range(0, 200):
                bag_table[i][0] = b_ids[i]
                bag_table[i][1] = degrees_bag[i]

            bt = np.argsort(bag_table[:,1]) #sort degree
            bag_table = bag_table[bt].tolist()
            bag_table.sort(key=lambda x:x[1],reverse=True)

            bag_b_ids = []
            for i in range(0, 200):
                bag_b_ids.append(int(bag_table[i][0]))
            #================cv 1 end=====================

            #================color=====================
            degrees_color = []
            linedata = dataset_color[idx*2+1]
            for i in range(1, len(linedata)):
                degrees_color.append(float(linedata[i].split(",")[0]))

            color_table = np.zeros([200,2])
            for i in range(0, 200):
                color_table[i][0] = b_ids[i]
                color_table[i][1] = degrees_color[i]

            bt = np.argsort(color_table[:,1]) #sort degree
            color_table = color_table[bt].tolist()
            color_table.sort(key=lambda x:x[1],reverse=True)

            color_b_ids = []
            for i in range(0, 200):
                color_b_ids.append(int(color_table[i][0]))
            #================color end=====================

            #================model1 + bag=================
            model1_bag_degree = []
            for i in range(0, 200):
                temp = degrees_model1[i] * 0.9 + degrees_color[i] * 0.1
                model1_bag_degree.append(temp)

            model1_bag_table = np.zeros([200,2])
            for i in range(0, 200):
                model1_bag_table[i][0] = b_ids[i]
                model1_bag_table[i][1] = model1_bag_degree[i]

            bt = np.argsort(model1_bag_table[:,1]) #sort degree
            model1_bag_table = model1_bag_table[bt].tolist()
            model1_bag_table.sort(key=lambda x:x[1],reverse=True)

            model1_bag_b_ids = []
            for i in range(0, 200):
                model1_bag_b_ids.append(int(model1_bag_table[i][0]))

            db = DB_Object("../Clothes.sqlite")
            match_data = db.fetch_data(num=3,target_id=idx+1)
            match_list = match_data[0][1]
            match_list = match_list.replace(';',',')
            match_list = match_list.split(',')

            m_ap_model1 += one_ap(b_ids)
            m_ap_bag += one_ap(bag_b_ids)
            m_ap_model1_bag += one_ap(model1_bag_b_ids)
            m_ap_color += one_ap(color_b_ids)


        map200_model1 = m_ap_model1 / num_test
        map200_bag = m_ap_bag / num_test
        map200_model1_bag = m_ap_model1_bag / num_test
        map200_color = m_ap_color / num_test
        
        print(map200_model1)
        print(map200_bag)
        print(map200_model1_bag)
        print(map200_color)
