# 给定一个表示 大整数 的整数数组 digits，其中 digits[i] 是整数的第 i 位数字。
# 这些数字按从左到右，从最高位到最低位排列。这个大整数不包含任何前导 0。
# 将大整数加 1，并返回结果的数字数组。


aaa = [9,3,4,5]
def plusOne(digits):
        a = 0

        for i in range(len(digits)):
            a= a + digits[i]*10**(len(digits)-i-1)

        a += 1
        new_digits = []

        for i in range(len(str(a))):
            new_digits.append(int(str(a)[i]))

        return new_digits

print(plusOne(aaa))

# a = 0
# for i in range(len(aaa)):
#     a= a + aaa[i]*10**(len(aaa)-i-1)



# print(a)