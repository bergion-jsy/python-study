"""
利用电脑物理环境噪声产生 [1, 100] 的均匀随机整数
不依赖 random 模块，只依靠物理噪声源
"""

import time
import os
import struct

# ========== 物理噪声源 ==========

def source_time_jitter() -> int:
    """
    噪声源 1：时间抖动
    利用 time.perf_counter() 的高精度计时器，
    读取最后几位小数位的不可预测性
    """
    # 多次计时，取小数部分的细微差异
    t1 = time.perf_counter()
    for _ in range(100):
        _ = 1 + 1
    t2 = time.perf_counter()
    delta = t2 - t1
    # 取小数部分后 6 位
    return int((delta % 0.000001) * 1_000_000) % 256


def source_cpu_noise() -> int:
    """
    噪声源 2：CPU 执行时间抖动
    利用 Python 的 id() 函数返回内存地址的随机性
    """
    # 创建对象，获取其内存地址
    addr1 = id(object())
    addr2 = id(object())
    # 内存地址的差异包含系统分配的随机性
    return (addr1 ^ addr2) % 256


def source_os_entropy() -> int:
    """
    噪声源 3：操作系统熵池
    读取 /dev/urandom（Unix）或 os.urandom
    底层利用硬件噪声（CPU热噪声、外围设备中断时间等）
    """
    # 读取 1 字节的随机数
    random_byte = os.urandom(1)
    return random_byte[0]  # 0~255


def source_process_time() -> int:
    """
    噪声源 4：进程时间噪声
    系统 clock 的高精度计时
    """
    t = time.process_time_ns()  # 纳秒级精度
    return (t >> 4) % 256       # 取部分位


# ========== 混合熵池 ==========

def collect_entropy() -> int:
    """
    混合多个噪声源，产生一个 0~255 的随机字节
    使用 XOR 混合，保持均匀性
    """
    e1 = source_time_jitter()
    e2 = source_cpu_noise()
    e3 = source_os_entropy()
    e4 = source_process_time()
    
    # XOR 混合四个熵源
    combined = e1 ^ e2 ^ e3 ^ e4
    return combined


# ========== 构造 [1, 100] 的均匀分布 ==========

def rand100() -> int:
    """
    利用物理噪声产生 [1, 100] 的均匀随机整数
    采用拒绝采样保证均匀性
    """
    while True:
        # 收集 7 个随机字节，构造一个 0~2^56-1 的数
        entropy_bytes = bytes([collect_entropy() for _ in range(7)])
        
        # 将 7 字节转换为大整数
        num = int.from_bytes(entropy_bytes, byteorder='big')
        
        # 我们需要 [1, 100]，用拒绝采样
        # 取一个接近 2^56 且是 100 的倍数的数作为阈值
        # 2^56 = 72057594037927936
        # 取 72057594037927900 作为阈值（100 的倍数）
        threshold = (2**56) // 100 * 100
        
        if num < threshold:
            return (num % 100) + 1


# ========== 测试 ==========

def test_uniformity():
    """统计检验：测试 100000 次，看分布"""
    from collections import Counter
    
    n = 100000
    results = [rand100() for _ in range(n)]
    counter = Counter(results)
    
    print(f"测试 {n} 次，每个数字期望出现约 {n//100} 次\n")
    
    # 打印统计
    counts = [counter[i] for i in range(1, 101)]
    min_count = min(counts)
    max_count = max(counts)
    avg_count = sum(counts) / 100
    
    print(f"最小值: {min_count}")
    print(f"最大值: {max_count}")
    print(f"平均值: {avg_count:.1f}")
    print(f"最大偏差: {max(abs(c - avg_count) for c in counts):.1f} ({max(abs(c - avg_count) for c in counts)/avg_count*100:.1f}%)")
    
    # 打印前 20 个结果
    print("\n前 20 次调用结果:")
    print([rand100() for _ in range(20)])


if __name__ == "__main__":
    print("=" * 50)
    print("物理随机数生成器 (基于系统物理环境噪声)")
    print("=" * 50)
    print()
    
    # 演示不同噪声源
    print("单个熵源示例 (每次调用都不同):")
    print(f"  时间抖动:    {[source_time_jitter() for _ in range(5)]}")
    print(f"  CPU 噪声:    {[source_cpu_noise() for _ in range(5)]}")
    print(f"  OS 熵池:     {[source_os_entropy() for _ in range(5)]}")
    print(f"  进程时间:    {[source_process_time() for _ in range(5)]}")
    print()
    
    print("Rand100() 结果 (基于物理噪声):")
    print(f"  {[rand100() for _ in range(10)]}")
    print()
    
    # 运行统计检验
    test_uniformity()
