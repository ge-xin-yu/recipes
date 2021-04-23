#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
------------------------------------------
    FileName:       redis_query.py
    Description:    redis缓存远程脚本查询
    Author:         LaoG
    Date:           2021-4-23：
------------------------------------------
"""
import sys
import argparse
from redis import Redis

conn = Redis(host="172.16.6.8", port="6001", decode_responses=True)
keys = conn.keys()
parser=argparse.ArgumentParser()
parser.add_argument('-l1',action='store_true')
parser.add_argument('-k','--key', type=str)
parser.add_argument('-f','--file')
parser.add_argument('-l1k')
parser.add_argument('-l2k')
args = parser.parse_args()
if args.l1:
    print(keys)

if args.key in keys:
    hkeys = conn.hkeys(args.key)
    for hkey in hkeys:
        print(hkey)

if args.l1k and args.l2k:
    print(conn.hget(args.l1k,args.l2k))  

conn.close()
