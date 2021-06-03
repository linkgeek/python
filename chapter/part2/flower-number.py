# 水仙花数

num = 1530

i = int(num / 100)
j = int(num / 10 % 10)
k = num % 10
result = pow(i, 3) + pow(j, 3) + pow(k, 3)

if num == result:
    print(str(num) + "是水仙花数")
else:
    print(str(num) + "不是水仙花数")