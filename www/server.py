#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, request, render_template ,jsonify
from home import *
from support import date_limit
import json

app = Flask(__name__)

#地市对应表
@app.route('/city', methods=['GET', 'POST'])
def city():
	if request.method == 'POST':
		row = request.get_data()
		dict1 = json.loads(row)
		return city_query(dict1)
	else:
		return 'Use the method POST please !!!'

#激活成功率（单个apn）
@app.route('/rate', methods=['GET', 'POST'])
def rate_a():
	dict2 = {}
	if request.method == 'POST':
		row = request.get_data()
		dict1 = json.loads(row)
		if dict1['type'] in ['15','60','1440']:
			if 'time_start' in dict1.keys():
				time_size = date_limit(dict1['type'],dict1['time_start'],dict1['time_end'])
				if time_size > 0:
					dict2['status'] = '3'
					return json.dumps(dict2)
				else:
					return rate_query(dict1)
			else:
				return rate_query(dict1)
		else:
			dict2['status'] = '2'
			return json.dumps(dict2)
	else:
		return 'Use the method POST please !!!'

#激活成功率（全省激活率前几或后几apn）
@app.route('/rate/sort', methods=['GET', 'POST'])
def rate_b():
	dict2 = {}
	if request.method == 'POST':
		row = request.get_data()
		dict1 = json.loads(row)
		if dict1['type'] in ['15','60','1440']:
			return rate_sort(dict1)
		else:
			dict2['status'] = '2'
			return json.dumps(dict2)
	else:
		return 'Use the method POST please !!!'

@app.errorhandler(404)
def not_found(error):
	dict2 = {}
	dict2['status'] = '1'
	return json.dumps(dict2)


if __name__ == '__main__':
    app.run(host='192.168.1.7',port=int('8999'))
