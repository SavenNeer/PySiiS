# -*- coding:utf-8 -*-
import numpy as np
import math

# 定义关于基础的数据包及其生成器

# 一组码元的数据采样包
class DataPack:

    def __init__(self):
        # 一组码元的个数
        self.grpsize = 10
        # 采样点间隔
        self.sampling_t = 0.01
        # 采样码元序列
        self.data = np.array([0,1],dtype=np.float32)
        # 采样基础序列
        self.t = []
        # 注释标注信息
        self.comments = {}
    
    def datagen(self,signal=[]):
        """生成信号"""
        # 检查信号的长度
        if signal is None or len(signal) != self.grpsize:
            # 不满足条件则单独生成规定长度的信号
            signal = self.signalgen()
        print(signal)
        signal = [ int(one) for one in signal ]
        self.comments["gen"] = signal
        # 生成采样点列表
        self.t = np.arange(0,self.grpsize,self.sampling_t)
        # 信号采样
        self.data = np.zeros(len(self.t),dtype=np.float32)
        for i in range(len(self.t)):
            # 向下取整 信号非0即1
            self.data[i] = signal[math.floor(self.t[i])]
        return (self.t,self.data) # 返回生成信号

    def signalgen(self,lenth=None):
        """任意长度的信号数字量随机生成器"""
        if lenth is None:
            lenth = self.grpsize
        return np.random.randint(0,2,lenth)



