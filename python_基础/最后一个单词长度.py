
t = "hello world"
l = "   fly me   to   the moon  "
k = "luffy is still               joy.  boy                   "





def lengthOfLastWord(s):
    i = len(s) - 1
    while i >= 0 and s[i] == ' ':
        i -= 1
    j = i
    while j >= 0 and s[j] != ' ':
        j -= 1
    return i - j

print(lengthOfLastWord(t))
print(lengthOfLastWord(l))
print(lengthOfLastWord(k))