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


# 原始信号包
pack = DataPack()
# 根据要求生成采样信号包
(x0,y0) = pack.datagen([1,0,1,0,1,0,1,0,1,0])

ax0 = fig.add_subplot(5, 1, 1)
ax0.set_title('原始信号波形', fontproperties=zhfont1, fontsize=10)
plt.axis([0, 10, -2, 2])
plt.plot(x0,y0, 'b')



# ASK调制信号
ASK = ASKcoder()
askpack = ASK.encode(pack)
(x1,y1) = (askpack.t,askpack.data)

ax1 = fig.add_subplot(5, 1, 2)
ax1.set_title('原始信号波形', fontproperties=zhfont1, fontsize=10)
plt.axis([0, 10, -2, 2])
plt.plot(x1,y1, 'b')




# 噪声信道
chn = CtlChannel()
outpack = chn.transport(askpack)
(x2,y2) = (outpack.t,outpack.data)

ax2 = fig.add_subplot(5, 1, 3)
ax2.set_title('通过信道后的波形', fontproperties=zhfont1, fontsize=10)
plt.axis([0, 10, -2, 2])
plt.plot(x2,y2,'b')



# 低通滤波去噪
nflt = NoiseFliter()
outpack = nflt.fliter(outpack)
(x3,y3) = (outpack.t,outpack.data)

ax3 = fig.add_subplot(5, 1, 4)
ax3.set_title('椭圆滤波后的波形', fontproperties=zhfont1, fontsize=10)
plt.axis([0, 10, -2, 2])
plt.plot(x3,y3,'b')


# 解码
pack = ASK.decode(outpack)
(x4,y4) = (pack.t,pack.data)

ax4 = fig.add_subplot(5, 1, 5)
ax4.set_title('2ASK滤波解码', fontproperties=zhfont1, fontsize=10)
plt.axis([0, 10, -0.5, 1.5])
plt.plot(x4,y4,'b')




############# 显示图像 ##############
plt.show()


