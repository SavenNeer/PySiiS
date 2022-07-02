from base.ask import DataPack

# 面向6+4模式的Haming校验代码
# Haming差错控制器

class HamErrCtl():

    ARQ_REPEAT_CMD = "repeat"

    def __init__(self):
        """初始化"""
        self.precode = []
        self.state = "ok"
 
    def hamingCal(self,pt):
        """根据haming规则异或计算"""
        # 必须保证len(pt)==10
        # 异或计算
        pt = [int(i) for i in pt]
        pt[0] = pt[2] ^ pt[4] ^ pt[6] ^ pt[8]
        pt[1] = pt[2] ^ pt[5] ^ pt[6] ^ pt[9]
        pt[3] = pt[4] ^ pt[5] ^ pt[6]
        pt[7] = pt[8] ^ pt[9]
        # 记录
        self.precode = pt
        # 返回
        return pt

    def errctl_encode(self, tc=[]):
        """Haming差错编码"""
        self.state = "encode"
        self.precode = []
        print("需要传输的码元:{}".format(tc))
        if len(tc) == 6:
            pt = [
                0,0,tc[0],0,tc[1],tc[2],tc[3],0,tc[4],tc[5]
            ]
            pt = self.hamingCal(pt)
            print("Haming编码后:{}".format(pt))
            # 生成信号
            pack = DataPack()
            pack.datagen(pt)
            return pack
        return None
    
    
    def errctl_decode(self, pack):
        """Haming差错解码"""
        self.state = "ok"
        if isinstance(pack,DataPack):
            # 获取数字序列
            pt = self.precode.copy() # 获取加密前的代码 - 保障校对
            print("pt:{}".format(pt))
            # ---
            pt0 = pack.comments["decode3"].copy() # 获取数据包的数据
            pt0 = [int(i) for i in pt0]
            print("pt0:{}".format(pt0))
            print("HamingDecoder接收到的原始序列:{}".format(pt0))
            hc0 = [int(pt0[i]) for i in [7,3,1,0]] # 数据包计算得校验码
            print("接受到的校验码:{}".format(hc0))
            # ---
            pt1 = self.hamingCal(pt0.copy()) # 计算其应有的Haming校验码
            hc1 = [int(pt1[i]) for i in [7,3,1,0]] # 数据包计算得校验码
            print("接收序列计算的校验码:{}".format(hc1))
            # 异或运算矫正
            qu = [8,4,2,1]
            index = 0
            for i in range(0,4):
                index += (qu[i] * (hc0[i] ^ hc1[i]))
            print("index == {}".format(index))
            if pt0 == pt: # 没有错误
                print("Haming Decode Check:Yes")
                return pack
            if index >= 1 and index <= 10:
                print("Haming Decode Check:Error on bit[{}]".format(index))
                # 纠错
                pack1 = DataPack()
                pack1.datagen(pt)
                pack1.comments = pack.comments
                pack1.comments["decode3"] = pt
                return pack1
        # 重传
        self.state = "ARQ"
        print("Haming Decode Check:ARQ")
        return pack # 返还原pack数据包不变

