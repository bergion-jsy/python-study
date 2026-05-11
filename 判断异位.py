# 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的 字母异位词。
from collections import Counter


s = input("请输入字符串s:")
t = input("请输入字符串t:")


# def judgement_heterotopy(s,t):
#     return  Counter(s) == Counter(t)

def judgement_heterotopy(s,t):
    char_1_count = {}
    char_2_count = {}

    
    for char in s:
            char_1_count[char] = char_1_count.get(char,0) + 1

    for char in t:
            char_2_count[char] = char_2_count.get(char,0) + 1

    print("char_1_count:",char_1_count)
    print("char_2_count:",char_2_count)
          
    return char_1_count == char_2_count
    

print(judgement_heterotopy(s,t))





                












