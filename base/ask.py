# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from math import pi
import scipy.signal as signal
from base.data import DataPack


class ASKcoder:

    def __init__(self):

        # 高频相干载波频率
        self.fc = 4000
        # 相干载波的采样(频率)倍数
        self.alpha = 20

        # 相干载波(encode生成)
        self.cc = []
        # 低通滤波器通带截止频率
        self.lowpassF = 2000
        # 相干定性阈值
        self.limit = 9

    def encode(self,pack=None):
        """对单个采样数据包进行ASK调制"""
        if isinstance(pack,DataPack):
            # 相干波采样频率
            fs = self.alpha * self.fc
            # 生成相干波
            cntall = int(pack.grpsize / pack.sampling_t)
            ts = np.arange(0, cntall/fs, 1/fs)
            # 相干载波
            self.cc = np.cos(np.dot(2 * pi * self.fc, ts))
            ook = pack.data * self.cc # 2ASK调制信号波
            pack.data = ook
            return pack # (采样序列,2ASK信号序列)
        return None

    def decode_stage1(self,pack):
        """stage1 : 相干解调"""
        pack.data = pack.data * (self.cc * 2)
        return pack
    
    def decode_stage2(self,pack):
        """stage2 : 低通滤波"""
        [b12, a12] = signal.ellip(5, 0.5, 60, (self.lowpassF * 2 / 80000),
                                btype='lowpass', analog=False, output='ba')
        pack.data = signal.filtfilt(b12, a12, pack.data)        
        return pack
    
    def decode_stage3(self,pack):
        """stage3 : 抽样判决"""
        detection_bpsk = np.zeros(len(pack.t), dtype=np.float32)
        flag = np.zeros(pack.grpsize, dtype=np.float32)
        # 平均每个码元内的采样数量
        avercode_smpt = int(1.00 / pack.sampling_t)
        # 逐个码元统计采样点的总数
        for i in range(pack.grpsize):
            tempF = 0
            for j in range(avercode_smpt):
                tempF = tempF + pack.data[i * avercode_smpt + j]
            if tempF > self.limit:
                flag[i] = 1
            else:
                flag[i] = 0
        # 根据每个码元内采样点的投票对信号二值化还原
        for i in range(pack.grpsize):
            if flag[i] == 0:
                for j in range(avercode_smpt):
                    detection_bpsk[i * avercode_smpt + j] = 0
            else:
                for j in range(avercode_smpt):
                    detection_bpsk[i * avercode_smpt + j] = 1
        # 记录信号
        pack.data = detection_bpsk
        pack.comments["decode3"] = flag.tolist().copy()
        return pack
    
    def decode(self,pack):
        """"2ASK解码"""
        pack = self.decode_stage1(pack)
        pack = self.decode_stage2(pack)
        pack = self.decode_stage3(pack)
        return pack





# pack = DataPack()
# (x0,y0) = pack.datagen([1,0,1,0,1,0,1,0,1,0])
# ASK = ASKencoder()
# (x,y) = ASK.encode(pack)

# # 初始化坐标绘图
# fig = plt.figure()
# zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')

# ax0 = fig.add_subplot(2, 1, 1)
# ax0.set_title('原始信号波形', fontproperties=zhfont1, fontsize=10)
# plt.axis([0, 10, -2, 2])
# plt.plot(x0,y0, 'b')

# ax1 = fig.add_subplot(2, 1, 2)
# ax1.set_title('2ASK调制结果', fontproperties=zhfont1, fontsize=10)
# plt.axis([0, 10, -2, 2])
# plt.plot(x,y,'b')

# plt.show()




