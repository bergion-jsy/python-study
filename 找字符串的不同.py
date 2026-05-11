# 给定两个字符串 s 和 t ，它们只包含小写字母。
# 字符串 t 由字符串 s 随机重排，然后在随机位置添加一个字母。
# 请找出在 t 中被添加的字母。

# word1 = input("请输入第一个字符串：")
# word2 = input("请输入第二个字符串：")


word1 = "cdtba"
word2 = "actl"


def find_different(word1,word2):
    len_word1 = len(word1)
    len_word2 = len(word2)
    min_len = min(len_word1,len_word2)
    result = ""

    for i in range(len_word1):
        for j in range(len_word2):
            if word1[i] == word2[j]:
                result += word1[i]
            else:
                result = result
    
    len_result = len(result)
    new_result = ""

    for i in range(len_word2):
        for j in range(len_result):
            if word2[i] == result[j]:
                new_result = word2[:i] + word2[:i+1]
            else:
                new_result = word2[i]
    
    return new_result


print(find_different(word1,word2))

