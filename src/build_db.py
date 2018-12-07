# from build_db import create_db
import sqlite3


class DB_Object(object):

	def __init__(self,db_file):
		self.conn = sqlite3.connect(db_file, check_same_thread=False)
		# self.data_file = db_file
		self.cursor = self.conn.cursor()
		self.cursor.execute('ATTACH "{}" AS db'.format(db_file))
		self.conn.commit()


	def create_t1(self):
		### table for dim_items.txt ###
		sql1 = '''
				DROP TABLE IF EXISTS t1
			   '''
		sql2 = '''
		CREATE TABLE t1 (
			ID INT NOT NULL,
			Cat_ID INT NOT NULL,
			Terms VARCHAR(255)
			);'''

		self.cursor.execute(sql1)
		self.cursor.execute(sql2)
		self.conn.commit()


	def create_t2(self):
		### table for dim fashion match sets.txt ###
		sql1 = '''
				DROP TABLE IF EXISTS t2
			   '''
		sql2 = '''
		CREATE TABLE t2 (
			Coll_ID INT NOT NULL,
			Item_list VARCHAR(155)
			);'''
		
		self.cursor.execute(sql1)
		self.cursor.execute(sql2)
		self.conn.commit()

	def create_t3(self):
		### table for user history.txt ###
		sql1 = '''
				DROP TABLE IF EXISTS t3
			   '''
		sql2 = '''
		CREATE TABLE t3 (
			User_ID INT NOT NULL,
			Item_ID INT NOT NULL,
			Create_at VARCHAR(10)
			);'''
		self.cursor.execute(sql1)
		self.cursor.execute(sql2)
		self.conn.commit()

	def close(self):

		self.conn.close()

	def insert_t1(self,f1):

		f = open(f1)
		data = []
		sql = '''INSERT INTO t1(ID, Cat_ID, Terms) 
				 VALUES (?,?,?)'''
		for line in f:
			line = line.split()
			if len(line)==3:
				item_id, cat_id, terms = line[0], line[1], line[2]
				data.append((item_id, cat_id, terms))
		self.cursor.executemany(sql,data)
		self.conn.commit()

	def insert_t2(self,f2):

		f = open(f2)
		data = []
		sql = '''INSERT INTO t2(Coll_ID,Item_list) 
				 VALUES (?,?)'''
		for line in f:
			line = line.split()
			if len(line)==2:
				coll_id, item_list = line[0], line[1]
				data.append((coll_id, item_list))
		self.cursor.executemany(sql,data)
		self.conn.commit()

	def insert_t3(self,f3):

		f = open(f3)
		data = []
		sql = '''INSERT INTO t3(User_ID,Item_ID,Create_at) 
				 VALUES (?,?,?)'''
		for line in f:
			line = line.split()
			if len(line)==3:
				user_id, item_id, create_at = line[0], line[1], line[2]
				data.append((user_id, item_id, create_at))
		self.cursor.executemany(sql,data)
		self.conn.commit()


if __name__ == "__main__":

### Initialization ###
	db = DB_Object("Clothes.sqlite")
	db.create_t1()
	db.create_t2()
	db.create_t3()

### Insert data into tables

	dir = "../data/"
	f1 = dir+"dim_items.txt"
	f2 = dir+"dim_fashion_matchsets.txt"
	# f3 = dir+"test_items.txt"
	f3 = dir+"user_bought_history.txt"

	db.insert_t1(f1)
	db.insert_t2(f2)
	db.insert_t3(f3)

	db.close()
