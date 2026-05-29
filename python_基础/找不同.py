def findInsertWords(s, t):
    # if s == '':
    #     return t
    # elif t == s[0] * (len(t)):
    #     return s[0]
    # else:
    #     if set(s) != set(t):    # 插入的是新字母
    #         for ch in t:
    #             if ch not in s:
    #                 return ch
    #     else:                   # 插入的是已有字母
    #         s_list = list(s)
    #         t_list = list(t)
    #         i = 0
    #         while i < len(s_list):
    #             if s_list[i] in t_list:
    #                 # 在t_list中找到第一个s_list[i]并删除
    #                 t_list.remove(s_list[i])
    #                 # 删除s_list[i]
    #                 s_list.pop(i)
    #                 # 不增加i，因为s_list长度变了，继续检查当前位置
    #             else:
                #  i += 1
            # return t_list[0]
    xor = 0
    for ch in s + t:
        xor ^= ord(ch)
    return chr(xor)
# ========== 非常长的测试例 ==========

# 1. 插入新字母（在开头）
s1 = "abcdefghijklmnopqrstuvwxyz"
t1 = "aabcdefghijklmnopqrstuvwxyz"
print(f"测试1: {findInsertWords(s1, t1)} (预期: 'a')")

# 2. 在超长字符串中间插入新字母
s2 = "a" * 1000 + "b" * 1000 + "c" * 1000
t2 = "a" * 1000 + "x" + "b" * 1000 + "c" * 1000
print(f"测试2: {findInsertWords(s2, t2)} (预期: 'x')")

# 3. 在4000长度重复字符串末尾插入已有字母
s3 = "aaaaabbbbbccccc" * 200
t3 = "aaaaabbbbbccccc" * 200 + "a"
print(f"测试3: {findInsertWords(s3, t3)} (预期: 'a')")

# 4. 在2000长度字符串中间插入已有字母
s4 = "hello" * 400
t4 = "hello" * 200 + "l" + "hello" * 200
print(f"测试4: {findInsertWords(s4, t4)} (预期: 'l')")

# 5. 插入新字符（数字和特殊符号）
s5 = "0123456789" * 500 + "!@#$%^&*()" * 300
t5 = "0123456789" * 500 + "?" + "!@#$%^&*()" * 300
print(f"测试5: {findInsertWords(s5, t5)} (预期: '?')")

# 6. s为空字符串
s6 = ""
t6 = "Z"
print(f"测试6: {findInsertWords(s6, t6)} (预期: 'Z')")

# 7. s只有一个字符，插入相同字符
s7 = "A"
t7 = "AA"
print(f"测试7: {findInsertWords(s7, t7)} (预期: 'A')")

# 8. 插入中文字符
s8 = "你好世界" * 200
t8 = "你好世界" * 100 + "呀" + "你好世界" * 100
print(f"测试8: {findInsertWords(s8, t8)} (预期: '呀')")

# 9. 插入Emoji
s9 = "😀😁😂🤣😃😄😅😆😉😊" * 150
t9 = "😀😁😂🤣😃😄😅😆😉😊" * 75 + "🥳" + "😀😁😂🤣😃😄😅😆😉😊" * 75
print(f"测试9: {findInsertWords(s9, t9)} (预期: '🥳')")

# 10. 终极压力测试：超长字符串（10万个字符）
s10 = "".join(chr(i % 95 + 32) for i in range(100000))
t10 = s10[:50000] + "~" + s10[50000:]
result10 = findInsertWords(s10, t10)
print(f"测试10: {result10} (预期: '~') ✅" if result10 == '~' else f"测试10: {result10} (预期: '~') ❌")

# 11. 插入重复字母在开头
s11 = "abc"
t11 = "aabc"
print(f"测试11: {findInsertWords(s11, t11)} (预期: 'a')")

# 12. 插入重复字母在末尾
s12 = "abc"
t12 = "abcc"
print(f"测试12: {findInsertWords(s12, t12)} (预期: 'c')")

print("\n=== 全部测试完成 ===")

