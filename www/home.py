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

#地市对应表
def city_query(dict1):
    dic = {}
    mysql = Mysql()
    if dict1['city'] == 'all':
        mysql.query('select rb_id,rb_name from sys_region_base')
    else:
        mysql.query('select rb_id,rb_name from sys_region_base where rb_name = "%s"' % dict1['city'])
    dic['data'] = mysql.result()
    mysql.close()
    dic['status'] = '0'
    dic['fields'] = 'region_id,地市'
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#激活成功率（单个apn）
def rate_query(dict1):
    dict_tb = {'15':'wl_c_pdp_make_i15','60':'wl_c_pdp_make_h1','1440':'wl_c_pdp_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,激活成功率'
    if 'time_start' in dict1.keys():
        mysql.query('select time_end,request_rate from %s \
        where gtp_cause = 128 and region_id = %s and apn = "%s" \
        and time_end >= "%s" and time_end <= "%s"' \
        % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_start'],dict1['time_end']))
    else:
        mysql.query('select time_end,request_rate from %s \
        where gtp_cause = 128 and region_id = %s and apn = "%s" \
        and time_end = "%s"' % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_end']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#激活成功率（全省激活率前几或后几apn）
def rate_sort(dict1):
    dict_tb = {'15':'wl_c_pdp_make_i15','60':'wl_c_pdp_make_h1','1440':'wl_c_pdp_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,apn,激活成功率'
    if dict1['num'] == '0':
        mysql.query('select time_end,apn,request_rate from %s \
        where gtp_cause = 128 and region_id = %s and time_end = "%s" order by request_rate %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort']))
    else:
        mysql.query('select time_end,apn,request_rate from %s \
        where gtp_cause = 128 and region_id = %s and time_end = "%s" order by request_rate %s limit %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort'],dict1['num']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#活跃用户数（单个apn）
def active_query(dict1):
    dict_tb = {'15':'wl_c_active_make_i15','60':'wl_c_active_make_h1','1440':'wl_c_active_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,活跃用户数'
    if 'time_start' in dict1.keys():
        mysql.query('select time_end,active_total from %s \
        where  region_id = %s and apn = "%s" \
        and time_end >= "%s" and time_end <= "%s"' \
        % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_start'],dict1['time_end']))
    else:
        mysql.query('select time_end,active_total from %s \
        where region_id = %s and apn = "%s" \
        and time_end = "%s"' % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_end']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#活跃用户数（全省激活率前几或后几apn）
def active_sort(dict1):
    dict_tb = {'15':'wl_c_active_make_i15','60':'wl_c_active_make_h1','1440':'wl_c_active_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,apn,活跃用户数'
    if dict1['num'] == '0':
        mysql.query('select time_end,apn,active_total from %s \
        where region_id = %s and time_end = "%s" order by active_total %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort']))
    else:
        mysql.query('select time_end,apn,active_total from %s \
        where region_id = %s and time_end = "%s" order by active_total %s limit %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort'],dict1['num']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#流量数（单个apn）
def traffic_query(dict1):
    dict_tb = {'15':'wl_c_traffic_make_i15','60':'wl_c_traffic_make_h1','1440':'wl_c_traffic_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,上行流量,下行流量,总流量'
    if 'time_start' in dict1.keys():
        mysql.query('select time_end,sum_ul,sum_dl,sum_total from %s \
        where  region_id = %s and apn = "%s" \
        and time_end >= "%s" and time_end <= "%s"' \
        % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_start'],dict1['time_end']))
    else:
        mysql.query('select time_end,sum_ul,sum_dl,sum_total from %s \
        where region_id = %s and apn = "%s" \
        and time_end = "%s"' % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['apn'],dict1['time_end']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json

#流量数（全省激活率前几或后几apn）
def traffic_sort(dict1):
    dict_tb = {'15':'wl_c_traffic_make_i15','60':'wl_c_traffic_make_h1','1440':'wl_c_traffic_make_d1'}
    dic = {}
    mysql = Mysql()
    mysql.query('select rb_name from sys_region_base where rb_id = %s' % dict1['region_id'])
    dic['city'] = mysql.result()
    dic['status'] = '0'
    dic['fields'] = '结束时间,apn,上行流量,下行流量,总流量'
    if dict1['num'] == '0':
        mysql.query('select time_end,apn,sum_ul,sum_dl,sum_total from %s \
        where region_id = %s and time_end = "%s" order by active_total %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort']))
    else:
        mysql.query('select time_end,apn,sum_ul,sum_dl,sum_total from %s \
        where region_id = %s and time_end = "%s" order by sum_total %s limit %s'\
         % (dict_tb.get(dict1['type']),dict1['region_id'],dict1['time_end'],dict1['sort'],dict1['num']))
    dic['data'] = mysql.result()
    mysql.close()
    result_json = json.dumps(dic,cls=CJsonEncoder)
    return result_json