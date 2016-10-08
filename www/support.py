#!/usr/bin/env python
#-*- coding:utf-8 -*-

import time

def date_limit(time_type,time_start,time_end):
	ts = time.mktime(time.strptime(time_start, '%Y-%m-%d %H:%M:%S'))
	te = time.mktime(time.strptime(time_end, '%Y-%m-%d %H:%M:%S'))
	if time_type == '15':
		t = te - ts - 6*60*60
		return t
	if time_type == '60':
		t = te - ts - 24*60*60
		return t
	if time_type == '1440':
		t = te - ts - 30*24*60*60
		return t
