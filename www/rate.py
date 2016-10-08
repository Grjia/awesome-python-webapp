#!/usr/bin/env python
#-*- coding:utf-8 -*-

from datetime import date,datetime
import mysql.connector
import json
from sql import Mysql

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def rate_i15(region_id,apn):
    dic = {}
    mysql = Mysql()
    mysql.query('select count(1) from wl_c_ps_rate where count_0 = 1')
    dic['count'] = mysql.result()
    mysql.query('select apn,time_start,time_end,count_0 from wl_c_ps_rate where count_0 = 1 limit 10')
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json
