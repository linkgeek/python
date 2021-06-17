import random

from lib.helper import Helper
from lib.eastmoney import EastMoney
from lib.mredis import MyRedis

def gen_insert_sql():
    cid = 1
    num = 0
    for s in range(1001, 1016):
        for c in range(1, 4):
            print(f'({s}, {cid}, {c}, {random.randint(30, 99)}),')
        num += 1
        if num % 5 == 0:
            cid += 1


a = 1.23456
b = 2.355
c = 3.5
d = 2.5
e = 3
f = 0.625
h = 510.050807

print('%.2f' % a)
print(Helper.float_format(a, 2))

print('%.2f' % b)
print(Helper.float_format(b, 2))

print('%.2f' % c)
print(Helper.float_format(c, 2))

print('%.2f' % d)
print(Helper.float_format(d, 2))

print('%.2f' % e)
print(Helper.float_format(e, 2))

print('%.2f' % f)
print(Helper.float_format(f, 2))


print(Helper.float_format(h, 2))
print(Helper.float_format(h, 2))
exit()

# str = 'liming李明'
str = str(1.0)
# print(len(str))
# print(len(str.encode('gb18030')))

# redisObj = MyRedis('u-3dmj-php.redis.rds.aliyuncs.com')
# val = redisObj.str_get('123')
