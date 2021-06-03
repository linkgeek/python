# 重复元素判定, set() 函数来移除所有重复元素
def all_unique(list):
    return len(list) == len(set(list))


x = [1, 1, 2, 2, 3, 2, 3, 4, 5, 6]
y = [1, 2, 3, 4, 5]
print(all_unique(x))  # False
print(all_unique(y))  # True


# 检查字符串占用的字节数
def byte_size(str):
    return len(str.encode('utf-8'))


print(byte_size(''))  # 0
print(byte_size('Hello World'))  # 11

# 打印 N 次字符串
n = 2
s = "python"
print(s * n)
# pythonpython

# 大写第一个字母
s = "hello world"
print(s.title())
# Hello World

# 首字母小写
def decapitalize(str):
    return str[:1].lower() + str[1:]


print(decapitalize('FooBar'))  # 'fooBar'
