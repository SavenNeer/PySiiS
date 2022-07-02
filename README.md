# PySiiS

## What is Framwork PySiiS ?

This is a simple basic communication system visualization framework that can be used to combine different types of communication system components.

``Created by SavenNeer @ sdust.cs.iot``

## Main Framwork

```
[data]
    =>差错控制输入
        =>数字调制输入
            =>可控误差信道
        =>数字调制输出
    =>差错控制输出
=>[data]
```

The framework implements a visual and componentized operation process based on ``matplotlib`` and its schematic is as follows:

![image](/imgs/image1.png)


## Generic Data Package

* The ``class DataPack`` in ``data.py`` is a generic stream-transporting package.

* Its built-in signal sampling configuration information and discrete sampling results. The format is ``numpy.ndarray`` and can be well used in related mathematical calculations.


## Error Control

* We provide Haming and CRC error controllers by default, you can design your own error control modules with reference to ``haming.py`` and ``crc.py``.

* We recommend that the error control module implement the ``class.errctl_encode(signals=[])`` method to complete the encoding of the digital signal and decode its output via ``class.errctl_decode(DataPack)``.

* You need to define the ``.state`` variable inside the modules to feed your ARQ status messages to your main program.

## Signal Conversion Stream

* The conversion list ``T=List()`` has been defined in the main program, you can pass the function addresses from the instantiated objects into the list, and the framework will automatically collect and visualize the output results of each component in the list.

* Note that you must ensure that the inputs and outputs of each function in ``T`` must be in ``DataPack`` format.

```python
# DataPack信号转换列表
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
```

## History Packets

* The ``class HisDataGrp`` is a dataset used to store discrete signal data for each stage. Its built-in method ``HisDataGrp.addData(DataPack)`` is used to add the resulting data internally.

* Note that you must ensure that each ``DataPack`` you pass in has the same sampling frequency.

## Dynamic Player

* ``class DynPlayer`` class for dynamic visual playback of ``HisDataGrp`` data. It is able to arrange the signal waveform plot sequentially in the order of the signals added by ``addData()`` to show the characteristics of the signals at different stages of processing.

* ``DynPlayer.setXX(pack.t)`` is used to set the signal drive stream. Pack.t is essentially a collection of points formed by the sampled abscissa of a waveform graph.

* ``DynPlayer.play(hisdata=HisDataGrp,xlims=(0,pack.grpsize))`` use ``matplotlib.pyplot`` to play the waveform graph. Does not automatically exit when playback is complete. To automatically exit the function, use the ``DynPlayer.autoplay()`` function.


## Example

![image](/imgs/image2.png)

## Contact Me

Email：``caoyiming233 [at] 126 dot com``
