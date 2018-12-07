#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 01:55:24 2018

@author: renwendi
"""
import sqlite3

"""
Schema of the database:

CREATE TABLE db.t1 (
			ID INT NOT NULL,
			Cat_ID INT NOT NULL,
			Terms VARCHAR(255)
			);
CREATE TABLE db.t2 (
			Coll_ID INT NOT NULL,
			Item_list VARCHAR(155)
			);
CREATE TABLE db.t3 (
			User_ID INT NOT NULL,
			Item_ID INT NOT NULL,
			Create_at VARCHAR(10)
			);

"""

class DB_Object(object):

	def __init__(self, db_file="./Clothes.sqlite"):
		self.conn = sqlite3.connect(db_file, check_same_thread=False)
		self.cursor = self.conn.cursor()
		# self.num = num
		# self.cat_id = cat_id
		# self.target_id = target_id
		# self.item_id = item_id

	def fetch_data(self,num=None, cat_id=None, target_id=None, item_id=None):

		if(num==1):        
			# EDIT YOUR SQL HERE
			sql = ''' 
				  SELECT * FROM t1;
				  '''
		if(num==2):
			sql = ''' 
			  SELECT * FROM t1 where t1.Cat_ID == {};
			  '''.format(cat_id)

		if(num==3):
			sql = ''' 
			  SELECT * FROM t2 where t2.Coll_ID == {};
			  '''.format(target_id)

		if(num==4):
			sql = ''' 
			  SELECT * FROM t1 where t1.ID == {};
			  '''.format(item_id)
		# find purchase history with id
		if(num==5):
			sql = ''' 
			  SELECT * FROM t3 where t3.item_id == {};
			  '''.format(item_id)
		#find all the item id at t3     
		if(num==6):
			sql = ''' 
				SELECT Item_ID FROM t3;
			  '''
	
		result = self.cursor.execute(sql).fetchall()

		return result
	### If you haven't set up the clothes database, please run the build_db.py before you move on

	# def excution(self, num=0, cat_id=None, target_id=None, item_id=None):

		