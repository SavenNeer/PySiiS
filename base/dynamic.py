import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from base.data import DataPack
import time
from threading import Thread

# 动态可视化模块
# 获取系统的数据提交 并进行演示


# 历史数据演示数据
class HisDataGrp:

    def __init__(self):
        # 历史数据存储区域
        self.stores = {}
        # 存储历史标记
        self.cntflag = 0
    
    def cls(self):
        """恢复所有存储清空"""
        self.stores = {}
        self.cntflag = 0
    
    def addData(self,pack=None):
        """添加序列化数据 内部自动复制pack.data"""
        if isinstance(pack,DataPack):
            self.stores[self.cntflag] = pack.data.copy()
            self.cntflag += 1


# 动态数据演示器
# FuncAnimation(fig, update, frames=np.arange(0, 2 * np.pi, 0.1), interval=50, blit=False, repeat=False)
class DynPlayer:

    def __init__(self):
        """初始化必要的参数"""
        self.interval = 50
        # self.blit = False
        self.blit = True
        self.repeat = False
        # 需要保证该参数是setXX的xx长度的正整数因子
        # 总播放次数
        self.playnum = 200
        # 多线程延迟plt持续时长s
        self.tt = 20
        # 
        self.xx = None
        self.fig = None
        self.hisdata = None

    def setXX(self,xx):
        """设置驱动数据帧流"""
        # 需要保证self.playnum是setXX的xx长度的正整数因子
        self.xx = xx # 这里需要传入pack.t
    
    def update_func(self,fram_index):
        """更新图像"""
        lenth = self.hisdata.cntflag
        col = ["b--","r-","c-","g-","b-","r--","c--","g--"]
        # 生成图像
        self.line = []
        for i in range(0,lenth):
            basey = i * 3
            ss = min(self.playgrp*fram_index,self.frmall)
            ee = min(self.playgrp*(fram_index+1),self.frmall)
            self.curfigs[i]["x"].extend(self.xx[ss:ee])
            self.curfigs[i]["y"].extend(basey+self.hisdata.stores[i][ss:ee])
            ln, = self.axis.plot(self.curfigs[i]["x"],self.curfigs[i]["y"],str(col[i]))
            self.line.append(ln)
        return self.line
    
    def init_line(self):  
        self.line.set_data([], [])
        return self.line,
    
    def inner_close(self,tt=20):
        """多线程关闭函数"""
        print("-- Play -- ")
        time.sleep(tt)
        print("-- Window Auto-Close -- ")
        plt.close()
    
    def autoplay(self,hisdata,xlims=(0,10)):
        """演示播放后自动停止"""
        thread1 = Thread(target=self.inner_close,args=(self.tt,))
        thread1.start()
        self.play(hisdata,xlims)
        
    def play(self,hisdata,xlims=(0,10)):
        """演示播放 - 需要自行添加更新逻辑"""
        if isinstance(hisdata,HisDataGrp):
            # 初始化记录表
            self.hisdata = hisdata
            self.fig = plt.figure()
            self.zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
            # 添加动态的演示数据
            self.curfigs = []
            for _ in range(0,hisdata.cntflag):
                self.curfigs.append({"x":[],"y":[]})
            #
            self.axis = plt.axes(xlim=xlims)
            # self.axis = plt.axes()
            self.line, = self.axis.plot([], [], lw = 3)  
            # 初始化演示程序
            self.frmall = len(self.xx)
            # 每次添加的点的个数
            self.playgrp = int(self.frmall / self.playnum)
            ani = FuncAnimation(self.fig,self.update_func,
                    frames=np.arange(0,self.playnum,1),
                    interval=self.interval,
                    init_func=self.init_line,
                    blit=self.blit,
                    repeat=self.repeat)
            # 开始演示
            plt.show()


