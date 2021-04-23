#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
------------------------------------------
    FileName:       redis-del.py
    Description:    redis手机缓存远程批量删除
    Author:         LaoG
    Date:           2021-4-23
------------------------------------------
"""

import redis
import argparse
from redis import Redis

conn = redis.Redis(host="172.16.6.8",port="6001",decode_responses=True)
parser=argparse.ArgumentParser()
parser.add_argument('-f', '--file')
args = parser.parse_args()

cust_hkeys_array = conn.hkeys('104$PK$CustPo')

if args.file:
    with open(args.file) as f:
        for line in f:
            #print('手机号: {:^13}'.format(line))
            line = line.strip()
            exist = 0
            for cust_hkey in cust_hkeys_array:
                if line in cust_hkey:
                    if conn.hdel('104$PK$CustPo',cust_hkey):
                        print("手机号:{:12} 缓存：{:30} 成功删除!".format(line,cust_hkey))
                    if not exist:
                        exist = 1
            #if count > 1:
            #    print(line)
            if not exist:
                print("手机号:{:12} 尚无缓存.".format(line))

