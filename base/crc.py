from base.ask import DataPack

# 面向6+4模式的CRC循环冗余校验代码

class CRCErrCtl():

    def __init__(self):
        """奇偶校验参数"""
        self.keys = [1,1,0,0,1] # 生成多项式(5位)
        self.state = "ok"
        self.precode = []
        # 错误对照表
        self.cmp = [
            [0, 1, 0, 1],
            [1, 1, 1, 0],
            [0, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    
    def crcCal(self,input=[]):
        """CRC计算 input(6 or 10 bit)"""
        # 6bit:编码用 10bit:解码用
        ori = input.copy()
        if len(input) == 6:
            print("crc-encode")
            ori.extend([0,0,0,0])
        # 计算
        ctl = [ int(ori[i]) for i in range(0,4) ]
        for index in range(4,10):
            ctl.append(int(ori[index]))
            if ctl[0] == self.keys[0]:
                ctl = [ int(ctl[i]^self.keys[i]) for i in range(1,5) ]
            else:
                ctl = [ int(ctl[i]) for i in range(1,5) ]
        # 返回计算得到的四位校验码
        return ctl

    def errctl_encode(self,tc=[]):
        """CRC编码"""
        self.state = "encode"
        self.precode = []
        print("需要传输的码元:{}".format(tc))
        if len(tc) == 6:
            # 计算并在尾部添加4位校验码
            tc.extend(self.crcCal(tc))
            print("CRC编码后:{}".format(tc))
            # 保存
            self.precode = tc.copy()
            # 生成信号
            pack = DataPack()
            pack.datagen(tc)
            return pack
        return None

    def errctl_decode(self, pack):
        """CRC解码检验"""
        self.state = "ok"
        if isinstance(pack,DataPack):
            # 获取数字序列
            pt = self.precode.copy() # 获取传输前的完整代码 - 保障校对
            # 获取传输后得到的10bit编码
            pt0 = pack.comments["decode3"].copy() # 获取数据包的数据
            pt0 = [int(i) for i in pt0]
            print("接受到的数据:{}".format(pt0))
            hc0 = self.crcCal(pt0) # 数据包计算得校验码
            print("重算校验码:{}".format(hc0))
            if hc0 == [0,0,0,0]:
                # 结果正确
                print("CRC Decode Check:Yes")
                return pack
            # 出错计算
            index = -1
            for i in range(0,len(self.cmp)):
                if hc0 == self.cmp[i]:
                    index = i
                    break
            if index >= 0:
                print("CRC Decode Check:Error on bit[{}]".format(index+1))
                # 修复
                pack1 = DataPack()
                pack1.datagen(pt)
                pack1.comments = pack.comments
                pack1.comments["decode3"] = pt
                return pack1
        # 重传
        self.state = "ARQ"
        print("CRC Decode Check:ARQ")
        return pack # 返还原pack数据包不变


