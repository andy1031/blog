"""
求一个0~255的随机数
"""


import random


# 1.函数有多个返回值
def get_random_color():
    A,B,C=255, 0, 0
    return A,B,C

ret = get_random_color()
print(ret, type(ret))


def get_random_color2():
    A=255, 0, 0
    return A

ret = get_random_color2()
print(ret, type(ret))




# 2.如何生成五位数的字母和数字随机组合的验证码, "A3bv7"
tmp_list = []
for i in range(5):
    u = chr(random.randint(65, 90))  # 生成大写字母
    l = chr(random.randint(97, 122))  # 生成小写字母
    n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

    tmp = random.choice([u, l, n])  # 随机选一个
    tmp_list.append(tmp)

print(tmp_list)
print("".join(tmp_list))
