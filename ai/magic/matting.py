"""
64 位操作系统  Python 和 pip 是 64 bit   "x86_64"、"x64" 或 "AMD64"内核
python -c "import platform;print(platform.architecture()[0]);print(platform.machine())"
"""

# coding=utf-8
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

import os
import paddlehub as hub

# 加载模型
huseg = hub.Module(name='deeplabv3p_xception65_humanseg')
base_dir = os.path.abspath(os.path.dirname(__file__))

# 获取当前文件目录
path = os.path.join(base_dir, 'images/')

# 获取文件列表
files = [path + i for i in os.listdir(path)]
print(files)

# 抠图
results = huseg.segmentation(data={'image': files})
for result in results:
    print(result)