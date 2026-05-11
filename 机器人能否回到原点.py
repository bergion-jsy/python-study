# 在二维平面上，有一个机器人从原点 (0, 0) 开始。
# 给出它的移动顺序，判断这个机器人在完成移动后是否在 (0, 0) 处结束。
# 移动顺序由字符串 moves 表示。字符 move[i] 表示其第 i 次移动。
# 机器人的有效动作有 R（右），L（左），U（上）和 D（下）。
# 如果机器人在完成所有动作后返回原点，则返回 true。
# 否则，返回 false。
# 注意：机器人“面朝”的方向无关紧要。 
# “R” 将始终使机器人向右移动一次，“L” 将始终向左移动等。此外，假设每次移动机器人的移动幅度相同。

def judgeCircle(move:str):
    r_move = 0
    l_move = 0
    u_move = 0
    d_move = 0

    for arr in move:
        if arr == "R":
            r_move += 1
        elif arr == "L":
            l_move += 1
        elif arr == "U":
            u_move += 1
        else:
            d_move += 1

    if r_move == l_move and u_move == d_move:
        return True
    else:
        return False
    
if __name__ == "__main__":
    print(judgeCircle("LL"))


