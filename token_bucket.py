# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from time import time
from threading import Lock

class token_bucket:
    def __init__(self, rate):
        #当在多线程中使用时，使用锁
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0
        self.last = 0
        
    def consume(self, amount=1):
        with self._consume_lock:            
            now = time()
            if self.last == 0:
                self.last = now
            elasped = now - self.last
            increment = int(elasped * self.rate)
            if increment:
                self.tokens += increment
                self.last = now
            self.tokens = min(self.tokens, self.rate)
            if self.tokens >= amount:
                self.tokens -= amount
            else:
                amount = 0
            return amount
            
#测试脚本
if __name__ == '__main__':
    test_list = [x for x in range(100)]
    #类初始化的值，比如50，应与打印结果一致
    rate_limit = leaky_bucket(50)
    start = time()
    for i in test_list:
        while not rate_limit.consume():
            pass
            
        print(i)
    end = time()
    print('平均速度为 {:.2f}次/s'.format(100/(end-start)))
    
    
    
    
    
    
    
    
    
    