import random


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


def test_float():
    print(round(a, 3))
    print(round(b, 2))
    print(round(f, 2))
    print(round(c))
    print(round(d))
    print('%.2f' % f)


# 保留2位小数
def float_format(num, decimals=2):
    str_num = str(num)
    a1, b1, c1 = str_num.partition('.')
    if len(c1) > decimals:
        cc = c1[:decimals]
        if int(c1[decimals]) >= 5:
            ccc = int(cc) + 1
        else:
            ccc = int(cc)
    else:
        ccc = c1

    # print(str(num) + '保留' + str(decimals) + '位小数：' + a1 + b1 + str(ccc))
    return a1 + b1 + str(ccc)


# test_float()
# print('..................................')
# print(float_format(a))
# print(float_format(a, 3))
# print(float_format(b))
# print(float_format(c))
# print(float_format(d))
# print(float_format(e))
# print(float_format(f))

# str = 'liming李明'
str = str(1.0)
# print(len(str))
print(len(str.encode('gb18030')))
