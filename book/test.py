from functools import reduce
def prod(L):
    def func(x,y):
        return x*y
    return reduce(func,L)


print('3 * 5 * 7 * 9 =')
print(prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('测试成功!')
else:
    print('测试失败!')