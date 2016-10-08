#!/usr/bin/env python
#-*- coding:utf-8 -*-

import mysql.connector

class Mysql:
	conn = ''
	cursor = ''
	def __init__(self):
		config = {
        		'host':'127.0.0.1',
        		'user':'root',
        		'password':'',
        		'port':3306,
        		'database':'wlws_187',
        		'charset':'utf8'
   		}
		try:
			self.conn = mysql.connector.connect(**config)
		except mysql.connector.Error as e:
        		print('connect fails!{}'.format(e))
        	self.cursor = self.conn.cursor()
		#self.query('SET NAME %s ' % charset)

	def query(self, sql):
		return self.cursor.execute(sql)

	def result(self):
		return self.cursor.fetchall()

	def close(self):
		self.cursor.close()
		self.conn.close()


