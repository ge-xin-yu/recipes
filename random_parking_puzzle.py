# -*- coding: utf-8 -*-
"""
..本程序解决在一个固定长度街道的路边平均停多少辆车的问题。
..此问题可以转化为一个递归问题。
..输出结果很有意思，车辆长度越小，道路的利用率越低；但并非车辆长度越大利用率越高。
..当车辆的宽度为道路长度的10分之一的时候，此时道路的利用率最高，其后就开始下降。利用率
..似乎存在一个正态分布的现象。
"""

import random

#道路长度及车辆宽度定义为全局变量
ROAD_LENGTH = 100
VEHICLE_WIDTH = 4.5

#low默认参数为0，之所以写在后面，是方便主函数调用，参数中可以不必写此参数。
def parking(high, low=0):
    if high - low < VEHICLE_WIDTH:
        return 0
    else:
        random_position = random.uniform(low, high-1)
        return (parking(random_position, low) + 1 + parking(high, random_position + VEHICLE_WIDTH))


def main(): 
    number_of_vehicles = 0
    #循环10000次，以得到精确的随机停车数量。
    for _ in range(10000):       
        number_of_vehicles += parking(ROAD_LENGTH)
    print('长度为 {} 米的道路可以停宽度为 {} 米的车 {:.2f} 辆'.format(STREET_LENGTH, VEHICLE_WIDTH, number_of_vehicles/10000))
    road_utilization_rate = number_of_vehicles/10000*VEHICLE_WIDTH/STREET_LENGTH
    print('道路平均利用率为 {:.2f}%'.format(road_utilization_rate*100))


if __name__ == '__main__':
    main()
