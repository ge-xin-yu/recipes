# -*- coding: utf-8 -*-
"""
多线程测试
"""

from queue import Queue, Empty
from threading import Thread
#from multiprocessing import Process, Pool
#from multiprocessing import Queue as ProcessQueue
import requests
from time import time


urls = [
       'https://www.baidu.com',
       'https://download.csdn.net/',
       'https://mp.weixin.qq.com/',
       'http://www.wps.cn/product/beta/',
       'https://www.etymonline.com/',
       'http://docs.python-requests.org/en/master/',
       'https://www.zhihu.com',
       'http://bbs.pinggu.org/',
       'http://www.tianya.cn/',
       'https://coderprog.com/',
       'https://zooqle.com/',    
       ]

header = {'User-Agent': 'Mozilla/5.0'}
#自定义线程数
thread_pool_size = 10
work_queue = Queue()
    
def worker(work_queue):
    while not work_queue.empty():
        url = work_queue.get()
        r = requests.get(url, headers=header)
        #print(r.text[:10])
        work_queue.task_done()

def main():
    threads = [Thread(target=worker, args=(work_queue,)) for _ in range(thread_pool_size)]
    for thread in threads:
        thread.start()
    #注意队列堵塞要在线程堵塞之前
    work_queue.join()
    #使用while循环，可以在堵塞线程的同时清空url列表，释放内存。
    #当然也可以使用for循环堵塞，但缺点是无法释放url列表所占内存。
    while threads:
        threads.pop().join()   
 
#测试脚本
if __name__ == '__main__':
    for url in urls:    
        work_queue.put(url)
    start = time()
    main()
    end = time()
    print('线程数：{}个\n总耗时：{:.2f} 秒'.format(thread_pool_size,end-start))  
 
