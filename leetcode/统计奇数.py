"""
给你两个非负整数 low 和 high，返回 [low, high] 范围内奇数的个数。
"""

class Solution:
    def countOdds(self, low: int, high: int) -> int:
        # (0~high 的奇数个数) - (0~(low-1) 的奇数个数)
        return (high + 1) // 2 - low // 2


# 测试用例
test_cases = [
    (3, 7, 3),    # [3,4,5,6,7] → 3个奇数: 3,5,7
    (2, 6, 2),    # [2,3,4,5,6] → 2个奇数: 3,5
    (1, 2, 1),    # [1,2]       → 1个奇数: 1
    (5, 5, 1),    # [5]         → 1个奇数: 5
    (0, 0, 0),    # [0]         → 0个奇数
    (0, 10, 5),   # [0..10]     → 5个奇数: 1,3,5,7,9
    (1, 10, 5),   # [1..10]     → 5个奇数: 1,3,5,7,9
    (8, 8, 0),    # [8]         → 0个奇数
    (0, 1, 1),    # [0,1]       → 1个奇数: 1
    (100, 200, 50), # [100..200] → 50个奇数
]

s = Solution()
all_pass = True
for low, high, expected in test_cases:
    result = s.countOdds(low, high)
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_pass = False
    print(f"{status} low={low}, high={high} -> {result} (预期: {expected})")

print(f"\n{'全部通过!' if all_pass else '有错误!'}")
