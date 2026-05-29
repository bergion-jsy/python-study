# =============================================
# 马尔可夫链 - 求平稳分布
# =============================================

import numpy as np


# =============================================
# 封装的函数：计算马尔可夫链的平稳分布
# =============================================
def stationary_distribution(P):
    """
    输入转移概率矩阵 P(n*n 的 numpy 数组或列表），
    返回平稳分布(numpy 数组）。
    如果无解（矩阵奇异导致无唯一概率解），返回 None。
    """
    P = np.array(P, dtype=float)
    n = P.shape[0]

    # 构造 A = P^T - I，然后最后一行替换为 [1, 1, ..., 1]
    A = P.T - np.eye(n)
    A[-1] = np.ones(n)

    # 常数向量 b：前 n-1 个为 0，最后一个为 1
    b = np.zeros(n)
    b[-1] = 1

    try:
        pi = np.linalg.solve(A, b)

        # 验证：π 所有分量 >= 0（概率非负）且 pi . P ~= pi
        if np.any(pi < -1e-10):
            return None
        pi = np.maximum(pi, 0)
        pi = pi / pi.sum()

        # 验证 pi . P ~= pi
        diff = np.abs(pi @ P - pi).sum()
        if diff > 1e-8:
            return None

        return pi

    except np.linalg.LinAlgError:
        return None


# =============================================
# 使用示例
# =============================================
if __name__ == "__main__":
    P = np.array([
        [0.1, 0.2, 0.7],
        [0.5, 0.4, 0.1],
        [0.1, 0.8, 0.1]
    ])

    pi = stationary_distribution(P)
    if pi is not None:
        print(f"平稳分布 = [{pi[0]:.4f}, {pi[1]:.4f}, {pi[2]:.4f}]")
    else:
        print("该马尔可夫链是暂态链，无平稳分布。")
