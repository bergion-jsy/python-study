# 给你两个字符串 haystack 和 needle ，请你在 haystack 字符串中找
# 出 needle 字符串的第一个匹配项的下标（下标从 0 开始）。
# 如果 needle 不是 haystack 的一部分，则返回  -1 。

haystack = "sadbutsad"
needle = "sad"

# def findFirstOccurrence(haystack,needle):

#     max_len = max(len(haystack),len(needle))
#     min_len = min(len(haystack),len(needle))

#     list_null = []

#     for i in range(max_len - min_len + 1):
#        if len(haystack) >= len(needle):
#         if needle == haystack[i:i+min_len]:
#             list_null.append(i)
#        elif len(haystack) < len(needle):
#         if haystack == needle[i:i+min_len]:
#             list_null.append(i)
       
#     if len(list_null) > 0 :
#       return list_null[0]
#     else:
#         return -1
    
    
# print(findFirstOccurrence(haystack,needle))

print(haystack.find(needle,2,6))
    

    

    



    