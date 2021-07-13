
import os
import sys

# 绝对路径
work_dir = os.path.dirname(os.path.abspath(__file__))
# 把当前路径切换到文件所在的路径
os.chdir(work_dir)

sys.path.append('../')
from lib.mmysql import Mmysqli

# 获取数据
mr = Mmysqli('192.168.7.105', 'root', 'steve201718', 'new_admin_dev')
sql = "select * from plat_config_detail where `key`='areashare' and configId=11"
data = mr.get_all(sql, {})
print(data)