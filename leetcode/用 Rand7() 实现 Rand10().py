# 给定方法 rand7 可生成 [1,7] 范围内的均匀随机整数，
# 试写一个方法 rand10 生成 [1,10] 范围内的均匀随机整数。
# 你只能调用 rand7() 且不能调用其他方法。请不要使用系统的 Math.random() 方法。
# 每个测试用例将有一个内部参数 n，即你实现的函数 rand10() 在测试时将被调用的次数。
# 请注意，这不是传递给 rand10() 的参数。


# ============================================
# 解法：拒绝采样
# 核心思想：
#   将 Rand7() 视为 7 进制的一位数字
#   用两次 Rand7() 构造 [1, 49] 的均匀分布
#   拒绝大于 40 的部分，剩余 [1, 40] 映射到 [1, 10]
# ============================================

class Solution:
    def rand10(self):
        """
        :rtype: int
        """
        while True:
            # (rand7()-1)*7 + rand7()
            # 第一次 rand7() 决定落在哪个 7 数块（高位）
            # 第二次 rand7() 决定块内偏移（低位）
            # 合起来是 [1, 49] 均匀分布
            num = (rand7() - 1) * 7 + rand7()
            
            # 拒绝采样：只取 [1, 40]
            if num <= 40:
                return (num - 1) % 10 + 1


# ============================================
# 拓展：利用系统硬件熵池构造真正的随机数
# 展示"随机数到底是怎么来的"
# ============================================

import os

def true_rand7():
    """
    用 os.urandom() 实现 Rand7()
    底层利用 CPU 热噪声、磁盘抖动等物理熵源
    """
    while True:
        byte = os.urandom(1)[0]  # 0~255
        if byte < 252:           # 252 是 7 的倍数
            return (byte % 7) + 1


def true_rand10():
    """
    用真随机种子实现 Rand10()
    """
    while True:
        num = (true_rand7() - 1) * 7 + true_rand7()
        if num <= 40:
            return (num - 1) % 10 + 1


# ============================================
# 均匀性验证
# ============================================

def test():
    from collections import Counter
    
    print("=" * 60)
    print("Rand7() → Rand10()  均匀性测试")
    print("=" * 60)
    
    n = 100000
    results = [true_rand10() for _ in range(n)]
    counter = Counter(results)
    
    avg = n // 10
    print(f"\n测试 {n} 次，每个数字期望 {avg} 次\n")
    print(f"{'数字':>4} | {'次数':>6} | {'偏差':>8}")
    print("-" * 30)
    
    max_dev = 0
    for i in range(1, 11):
        dev = (counter[i] - avg) / avg * 100
        max_dev = max(max_dev, abs(dev))
        bar = "█" * (counter[i] // 150)
        print(f"{i:>4} | {counter[i]:>6} | {dev:>+7.2f}% {bar}")
    
    print(f"\n最大偏差: {max_dev:.2f}%")
    print("判定: ✅ 通过" if max_dev < 5 else "判定: ❌ 不通过")


if __name__ == "__main__":
    test()
