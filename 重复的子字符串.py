# 给定一个非空的字符串 s ，检查是否可以通过由它的一个子串重复多次构成。
from math import gcd 
from functools import reduce

# s = "abcabc"
l ="babbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbbbabbaaabbb"
k = "abbaccabbacc"
def judgement_heterotopy(s):

    result = {}

    for char in s:
        result[char] = result.get(char,0) + 1

    for key,val in result.items():
        if val <= 1:
            return False

    values = list(result.values())
    gcd_value = reduce(gcd,values)

    other_result = {}
    for i in range(min(len(s)//gcd_value,gcd_value)-1):
        other_result[s[i]] = other_result.get(s[i],0) + 1
        other_result[s[len(s)-i-1]] = other_result.get(s[len(s)-i-1],0) + 1
    
    end_result = {}
    for key,val in other_result.items():
        end_result[key] = other_result.get(key,0) + val
    
    n = sum(other_result.values()) + max(end_result.values()) - min(end_result.values())

    if gcd_value == 1:
        return False
        
    if len(s)%gcd_value != 0:
        return False
    
    sub_len = len(s)//gcd_value

    if s[:gcd_value]*int(sub_len) == s or s[:sub_len]*int(gcd_value) == s or s[:n]*(len(s)//n) == s:
        return True
    else:
        return False
    
print(judgement_heterotopy(k))

# result = {}
# for char in l:
#         result[char] = result.get(char,0) + 1

# values = list(result.values())
# gcd_value = reduce(gcd,values)
# sub_len = len(l)//gcd_value
# sub_str = l[:gcd_value]
# print(len(l))
# print(gcd_value)
# print(sub_str)
# print(values)

# result = {}

# for char in s:
#     result[char] = result.get(char,0) + 1


# values = list(result.values())
# gcd_value = reduce(gcd,values)

# other_result = {}
# for i in range(min(len(s)//gcd_value,gcd_value)-1):
#     other_result[s[i]] = other_result.get(s[i],0) + 1
#     other_result[s[len(s)-i-1]] = other_result.get(s[len(s)-i-1],0) + 1
    
# end_result = {}
# for key,val in other_result.items():
#     end_result[key] = other_result.get(key,0) + val
    
# n = sum(other_result.values()) + max(end_result.values()) - min(end_result.values())
# print(n)


    



    

        