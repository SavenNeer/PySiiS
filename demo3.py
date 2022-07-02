# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib

from base.ask import ASKcoder
from base.channel import CtlChannel,NoiseFliter
from base.data import DataPack
from base.dynamic import HisDataGrp,DynPlayer


# 实例化各类转换器
ASK = ASKcoder()
chn = CtlChannel()
nflt = NoiseFliter()
# 实例化历史数据存储器
hisdata = HisDataGrp()
# 实例化动态播放器
dplayer = DynPlayer()
# 原始信号包
pack = DataPack()

# 中央转换函数
T = [
    ASK.encode, # ASK编码
    chn.transport, # 信道传输
    nflt.fliter, # 噪声过滤
    ASK.decode_stage1, # 相干解调
    ASK.decode_stage2, # 低通滤波
    ASK.decode_stage3  # 抽样判决
]
lenth = len(T)
# 一共lenth+1个图

# 根据要求生成采样信号包
pack.datagen([1,0,1,0,1,0,1,0,1,0])
# pack.datagen()
# 添加信号到hisdata
hisdata.addData(pack)

# [2..lenth+1]
for i in range(2,lenth+2):
    # 数据转换
    pack = T[i-2](pack)
    # 添加数据
    hisdata.addData(pack)
    print(pack.comments)


# 设置动态播放器驱动流
dplayer.setXX(pack.t)

print("play hisdata")

# 播放传输过程
# dplayer.play(hisdata=hisdata,xlims=(0,pack.grpsize))
dplayer.autoplay(hisdata=hisdata,xlims=(0,pack.grpsize))

