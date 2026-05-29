# 你现在是一场采用特殊赛制棒球比赛的记录员。
# 这场比赛由若干回合组成，过去几回合的得分可能会影响以后几回合的得分。
# 比赛开始时，记录是空白的。
# 你会得到一个记录操作的字符串列表 ops，其中 ops[i] 是你需要记录的第 i 项操作，ops 遵循下述规则：
# 整数 x - 表示本回合新获得分数 x
# "+" - 表示本回合新获得的得分是前两次得分的总和。题目数据保证记录此操作时前面总是存在两个有效的分数。
# "D" - 表示本回合新获得的得分是前一次得分的两倍。题目数据保证记录此操作时前面总是存在一个有效的分数。
# "C" - 表示前一次得分无效，将其从记录中移除。题目数据保证记录此操作时前面总是存在一个有效的分数。
# 请你返回记录中所有得分的总和。

ops = ["5","-2","4","C","D","9","+","+"]
#27

def calPoint(operations:list):
    operation_element = ["C","D","+"]
    target_point = []

    for arr in operations:
        if arr in operation_element:
            if arr == "C":
                del target_point[-1]
            elif arr == "+":
                target_point.append(target_point[-1] + target_point[-2])
            else:
                target_point.append(target_point[-1]*2)
        else:
            target_point.append(int(arr))
    
    total = sum(target_point)

    return total

print(calPoint(ops))
