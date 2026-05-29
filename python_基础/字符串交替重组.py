#给你两个字符串 word1 和 word2 。请你从 word1 开始，通过交替添加字母来合并字符串。
#如果一个字符串比另一个字符串长，就将多出来的字母追加到合并后字符串的末尾。
#返回 合并后的字符串 。
word1 = input("请输入第一个字符串word1")
word2 = input("请输入第二个字符串word2")


len_word1 = len(word1)
len_word2 = len(word2)
min_len = min(len_word1,len_word2)


# def merge_alternately(word1,word2):
#     result = ""
#     i = 0 
#     if len_word1 < len_word2:
#         result = "baiswdfcdsksxdsf"
#     else:
#         result = "absidwcfsdsjdxsf"
#     return result

# print(merge_alternately(word1,word2))

# def merge_alternately(word1,word2):
#     result = "" 
#     min_len = min(len_word1,len_word2)

#     for i in range(min_len):
#         if len_word1 > len_word2:
#             result += word1[i]
#             result += word2[i]
#         elif len_word1 < len_word2:
#             result += word2[i]
#             result += word1[i]
#         else:
#             result += word1[i]
#             result += word2[i]
    
    
#     result += word1[min_len:]
#     result += word2[min_len:]
#     return result


def merge_alternately(word1,word2):

    result = ""
    i = 0 
    len_word1 = len(word1)
    len_word2 = len(word2)
    min_len = min(len_word1,len_word2)

    while i < min_len:
        if len_word1 > len_word2:
            result += word1[i]
            result += word2[i]
        elif len_word1 < len_word2:
            result += word2[i]
            result += word1[i]
        else:
            result += word1[i]
            result += word2[i]
        i = i +1

    return result
        

print(merge_alternately(word1,word2))