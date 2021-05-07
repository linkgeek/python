# 引入同级文件
import test_a

# 直接同级目录下的文件
import testFile.test_c

# 引入不同级
import sys
sys.path.append('..')
from string.test_d import d

print('zhehsi test_b')
test_a.a()
testFile.test_c.c()

d()
