"""
利用鼠标轨迹产生真随机数
需要安装: pip3 install pyautogui
"""

import time
import math

try:
    import pyautogui
except ImportError:
    print("请先安装: pip3 install pyautogui")
    print("演示模式: 使用时间抖动")
    pyautogui = None


def mouse_random():
    """
    利用鼠标位置和时间的不可预测性产生随机数
    原理：人类无法精确控制鼠标轨迹，每次移动都有微小差异
    """
    if pyautogui is None:
        # 降级：使用时间抖动
        t = time.time_ns()
        return (t >> 4) % 100 + 1
    
    # 记录起始时间和鼠标位置
    x1, y1 = pyautogui.position()
    t1 = time.perf_counter_ns()
    
    # 等待 10 毫秒，让鼠标可能移动
    time.sleep(0.01)
    
    # 记录结束状态
    x2, y2 = pyautogui.position()
    t2 = time.perf_counter_ns()
    
    # 计算差值，利用微小的不确定性
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    dt = t2 - t1
    
    # 混合各种噪声
    noise = (dx * 1000003 + dy * 1000033 + (dt % 1000) * 10069) % 100
    return noise + 1


def demo():
    print("=" * 50)
    print("鼠标物理随机数生成器")
    print("=" * 50)
    print()
    print("请随意移动鼠标...")
    print()
    
    for i in range(10):
        num = mouse_random()
        print(f"  第 {i+1:2d} 次: {num}")
        time.sleep(0.3)


if __name__ == "__main__":
    demo()
