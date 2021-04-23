#!/bin/python


# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    FileName:       tcp_link_ar.py
    Description:    提取 tcp_link_ar.log 日志中的产权每日连接数据，并写入oracle库。 
    Author:         LaoG
    Date:           2021-4-23
----------------------------------------------------
"""


import calendar
import cx_Oracle
from datetime import datetime

def datetime_parse(line):
    datetime_array = line.split()
    year = datetime_array[5]
    month = list(calendar.month_abbr).index(datetime_array[1])
    day = datetime_array[2]
    hms = datetime_array[3]
    datetime_str = "{}-{}-{} {}".format(year,month,day,hms)
    return datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S')

def db_write(data):
    conn = cx_Oracle.connect('python/python@172.16.23.73:11521/ora11g')
    curs = conn.cursor()
    sql = 'INSERT INTO TCP_LINK_AR (DATETIME,CLOSE_WAIT,CLOSING,ESTABLISHED,FIN_WAIT1,FIN_WAIT2,LAST_ACK,LISTEN,SYN_RECV,SYN_SENT,TIME_WAIT) VALUES (:DATETIME,:CLOSE_WAIT,:CLOSING,:ESTABLISHED,:FIN_WAIT1,:FIN_WAIT2,:LAST_ACK,:LISTEN,:SYN_RECV,:SYN_SENT,:TIME_WAIT)'
    curs.execute(sql,data)    
    conn.commit()
    curs.close()
    conn.close()

week = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
data = {
    'DATETIME':0,
    'CLOSE_WAIT':0,
    'CLOSING':0,
    'ESTABLISHED':0,
    'FIN_WAIT1':0,
    'FIN_WAIT2':0,
    'LAST_ACK':0,
    'LISTEN':0,
    'SYN_RECV':0,
    'SYN_SENT':0,
    'TIME_WAIT':0
}

start = 1
with open('tcp_link_ar.log') as f:
    for line in f:
        line = line.strip()
        if line:
            if line.split()[0] in week:
                if start:
                    data['DATETIME'] = datetime_parse(line)
                    start = 0
                else:
                    #for key in data:
                    #    print("{:15}: {}".format(key,data[key]))
                    db_write(data)
                    for key in data:
                        data[key] = 0
                    data['DATETIME'] = datetime_parse(line)
            else:
                column_name = line.split()[0]
                column_value = line.split()[1]
                data[column_name] = column_value

db_write(data)
#for key in data:
#    print("{:15}: {}".format(key,data[key]))
