# -*- coding: utf-8 -*-
"""
令牌桶（单速单桶）
"""

from time import time
from threading import Lock

class token_bucket:
    def __init__(self, rate):
        #当在多线程中使用时，使用锁；如普通环境，此锁无需。
        self._consume_lock = Lock()
        self.rate = rate
        self.tokens = 0
        self.last = 0
        
    def consume(self, amount=1):
        #对于非多线程环境，不必增加以下加锁语句；如是，需加锁，以防止多个线程同时对以下参数进行修改。
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
    rate_limit = token_bucket(50)
    start = time()
    for i in test_list:
        while not rate_limit.consume():
            pass            
        print(i)
    end = time()
    print('平均速度为 {:.2f}次/s'.format(100/(end-start)))
    
    
    
    
