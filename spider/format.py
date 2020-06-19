
#省略字段名传递位置参数
print('我叫{},今年{}岁！'.format('小明', 18))
###########################
# 我叫小明,今年18岁！

#花括号个数可以少于位置参数的个数
print('我爱吃{}和{}。'.format('香蕉', '苹果', '大鸭梨'))
###########################
# 我爱吃香蕉和苹果。

#花括号个数多于位置参数的个数则会报错
print('我还吃{}和{}。'.format('西红柿'))
###########################
# Traceback (most recent call last):
#    File "E:/python文件夹/jiujiu.py", line 5, in <module>
#      print('我还吃{}和{}。'.format('西红柿'))
# IndexError: tuple index out of range

a = "Python"
b = "="
c = ">"
print("{0:{1}{3}{2}}".format(a, b, 25, c))
print("{0:=>25}".format(a, b, 25, c))