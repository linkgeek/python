import random

from lib.helper import Helper
from lib.eastmoney import EastMoney

print(EastMoney.get_realtime_rise_page(161725))
exit()

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

a3 = Helper.float_format(a, 4)
if a3 > 1.0:
    print('11')
print(a3)
exit()

# str = 'liming李明'
str = str(1.0)
# print(len(str))
print(len(str.encode('gb18030')))
