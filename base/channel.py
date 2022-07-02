# -*- coding:utf-8 -*-
import numpy as np
from math import pi
import scipy.signal as signal
from base.data import DataPack

# 可控误差信道

class CtlChannel:

    def __init__(self):
        """初始化必要参数"""
        self.snr = 5
    
    def awgn(self,y):
        """定义加性高斯白噪声"""
        snrs = 10 ** (self.snr / 10.0)
        xpower = np.sum(y ** 2) / len(y)
        npower = xpower / snrs
        return np.random.randn(len(y)) * np.sqrt(npower) + y
    
    def transport(self,pack):
        """经过信道-产生噪声"""
        if isinstance(pack,DataPack):
            pack.data = self.awgn(pack.data)
            return pack
        return None



# 去噪过滤器
class NoiseFliter():

    def __init__(self):
        # 带通椭圆滤波器 通带范围
        self.ellipticFLT = [2000,6000]
    
    def fliter(self,pack):
        # 带通椭圆滤波器
        [b11, a11] = signal.ellip(5, 0.5, 60,
                                [self.ellipticFLT[0] * 2 / 80000,
                                self.ellipticFLT[1] * 2 / 80000],
                                btype='bandpass', analog=False, output='ba')
        # 通过带通滤波器滤除带外噪声
        pack.data = signal.filtfilt(b11, a11, pack.data)
        return pack
      





