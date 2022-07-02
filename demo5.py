# -*- coding:utf-8 -*-
# import matplotlib.pyplot as plt
# import matplotlib

from base.ask import ASKcoder
from base.channel import CtlChannel,NoiseFliter
from base.data import DataPack
from base.dynamic import HisDataGrp,DynPlayer
from base.haming import HamErrCtl
from base.crc import CRCErrCtl


# 实例化各类转换器
ASK = ASKcoder()     # ASK调制解调器
chn = CtlChannel()   # 噪音通道
nflt = NoiseFliter() # 噪声过滤器
hmctl = HamErrCtl()  # Haming差错控制器
crctl = CRCErrCtl()  # CRC差错控制器
# 实例化历史数据存储器
hisdata = HisDataGrp()
# 实例化动态播放器
dplayer = DynPlayer()

# 随机生成信号
pack = DataPack()
pack.datagen()
randsignal = pack.comments["gen"][0:6]

# Haming差错编码
# pack = hmctl.errctl_encode([1,1,0,1,0,1])
pack = hmctl.errctl_encode(randsignal)
# CRC差错编码
# pack = crctl.errctl_encode([1,0,1,0,0,1])
# pack = crctl.errctl_encode(randsignal)
if isinstance(pack,DataPack):
    # 添加信号到hisdata
    hisdata.addData(pack)

    # 中央转换函数
    T = [
        ASK.encode, # ASK编码
        chn.transport, # 信道传输
        nflt.fliter, # 噪声过滤
        ASK.decode_stage1, # 相干解调
        ASK.decode_stage2, # 低通滤波
        ASK.decode_stage3, # 抽样判决
        hmctl.errctl_decode, # Haming差错控制
        # crctl.errctl_decode, # CRC差错控制
    ]
    lenth = len(T)
    # 一共lenth+1个图

    # [2..lenth+1]
    for i in range(2,lenth+2):
        # 数据转换
        pack = T[i-2](pack)
        # 添加数据
        hisdata.addData(pack)
        # print(pack.comments)

    # Haming差错控制结果
    if hmctl.state == "ARQ":
        print("ARQ-Haming要求重传")
    
    # CRC差错控制结果
    if crctl.state == "ARQ":
        print("ARQ-CRC要求重传")

    # 设置动态播放器驱动流
    dplayer.setXX(pack.t)

    print("play hisdata")

    # 播放传输过程
    dplayer.play(hisdata=hisdata,xlims=(0,pack.grpsize))
    # dplayer.autoplay(hisdata=hisdata,xlims=(0,pack.grpsize))

