# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib

from base.ask import ASKcoder
from base.channel import CtlChannel,NoiseFliter
from base.data import DataPack


# 初始化坐标绘图
fig = plt.figure()
# 适配汉字
zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')


# 实例化各类转换器
ASK = ASKcoder()
chn = CtlChannel()
nflt = NoiseFliter()

T = [
    ASK.encode,
    chn.transport,
    nflt.fliter,
    ASK.decode_stage1,
    ASK.decode_stage2,
    ASK.decode_stage3
]
lenth = len(T)
# 一共lenth+1个图


# 原始信号包
pack = DataPack()
# 根据要求生成采样信号包
(x0,y0) = pack.datagen([1,0,1,0,1,0,1,0,1,0])
# [1]
ax = fig.add_subplot(lenth+1,1,1)
ax.set_title("原始图像", fontproperties=zhfont1, fontsize=5)
plt.axis([0, 10, -2, 2])
plt.plot(x0,y0,'b')


# [2..lenth+1]
for i in range(2,lenth+2):
    pack = T[i-2](pack)
    ax = fig.add_subplot(lenth+1,1,i)
    ax.set_title(str(i), fontproperties=zhfont1, fontsize=5)
    plt.axis([0, 10, -2, 2])
    plt.plot(pack.t,pack.data, 'b')


plt.show()


