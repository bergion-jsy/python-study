"""
手势识别项目 — 演示版
使用 MediaPipe + PyTorch (MPS 加速)
无需摄像头，用模拟数据验证深度学习环境

验证目标：
  1. PyTorch + MPS (Apple GPU) 是否正常工作
  2. 神经网络训练流程是否完整
  3. 推理速度是否达到预期
"""

import torch
import torch.nn as nn
import numpy as np
import time

# ============================================
# 第一部分：设备检测
# ============================================

print("=" * 50)
print("🖐️  手势识别 — 深度学习环境验证")
print("=" * 50)
print()

# 检测 MPS
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print(f"✅ MPS (Apple Metal) 可用")
    print(f"   设备名称: {torch.mps.get_device_name() if hasattr(torch.mps, 'get_device_name') else 'Apple GPU'}")
else:
    device = torch.device("cpu")
    print(f"⚠️  MPS 不可用，使用 CPU")

print(f"   设备类型: {device}")
print(f"   PyTorch 版本: {torch.__version__}")
print()

# ============================================
# 第二部分：定义神经网络
# ============================================

class GestureNet(nn.Module):
    """
    手势分类网络
    输入：21 个手部关键点 (x, y) → 42 维
    输出：6 种手势类别
    """
    def __init__(self, num_classes=6):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(42, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.2),
            
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2),
            
            nn.Linear(64, num_classes)
        )
    
    def forward(self, x):
        return self.net(x)


# ============================================
# 第三部分：生成模拟数据
# ============================================

def generate_synthetic_data(n_samples=500):
    """
    生成模拟的手部关键点数据
    
    每种手势的关键点坐标有特定的分布模式：
      拳头 👊  → 所有手指弯曲（指尖靠近手掌）
      手掌 ✋  → 所有手指伸直（指尖远离手掌）
      食指 ☝️  → 仅食指伸直
      胜利 ✌️  → 食指和中指伸直
      点赞 👍  → 大拇指伸直，其余弯曲
      OK   👌  → 大拇指和食指形成圆圈
    """
    np.random.seed(42)
    torch.manual_seed(42)
    
    data = []
    labels = []
    
    # 每种手势的典型关键点模式（简化版）
    # 每个手势定义一个 42 维的"中心点"和"噪声范围"
    gesture_centers = {
        0: np.array([0.5]*42 + [0.1]*0),  # 拳头：所有点集中在中心
        1: np.array([0.5]*42 + [0.3]*0),  # 手掌：所有点分散
        2: np.array([0.5]*42 + [0.2]*0),  # 食指：特定模式
        3: np.array([0.5]*42 + [0.2]*0),  # 胜利：特定模式
        4: np.array([0.5]*42 + [0.2]*0),  # 点赞：特定模式
        5: np.array([0.5]*42 + [0.2]*0),  # OK：特定模式
    }
    
    # 实际生成：每个手势用不同的随机分布
    for gesture_id in range(6):
        for _ in range(n_samples // 6):
            # 生成随机关键点（模拟不同手势的差异）
            if gesture_id == 0:  # 拳头：所有点聚集
                landmarks = np.random.normal(0.45, 0.05, 42)
            elif gesture_id == 1:  # 手掌：所有点分散
                landmarks = np.random.normal(0.55, 0.15, 42)
            elif gesture_id == 2:  # 食指：部分手指突出
                landmarks = np.random.normal(0.5, 0.1, 42)
                landmarks[0:2] += 0.3  # 食指指尖突出
            elif gesture_id == 3:  # 胜利
                landmarks = np.random.normal(0.5, 0.1, 42)
                landmarks[0:4] += 0.25  # 食指和中指突出
            elif gesture_id == 4:  # 点赞
                landmarks = np.random.normal(0.5, 0.1, 42)
                landmarks[0:2] += 0.2   # 大拇指突出
            else:  # OK
                landmarks = np.random.normal(0.5, 0.1, 42)
                landmarks[0:2] += 0.15
                landmarks[4:6] += 0.15
            
            # 裁剪到合理范围 [0, 1]
            landmarks = np.clip(landmarks, 0, 1)
            data.append(landmarks)
            labels.append(gesture_id)
    
    data = torch.tensor(np.array(data), dtype=torch.float32)
    labels = torch.tensor(np.array(labels))
    
    # 打乱
    indices = torch.randperm(len(data))
    data = data[indices]
    labels = labels[indices]
    
    return data, labels


# ============================================
# 第四部分：训练模型
# ============================================

def train():
    print("\n📌 第一步：生成模拟数据")
    data, labels = generate_synthetic_data(600)
    
    # 划分训练集和测试集
    n_train = 500
    train_data = data[:n_train].to(device)
    train_labels = labels[:n_train].to(device)
    test_data = data[n_train:].to(device)
    test_labels = labels[n_train:].to(device)
    
    print(f"   训练集: {n_train} 条")
    print(f"   测试集: {len(data) - n_train} 条")
    print(f"   特征维度: {data.shape[1]}")
    print(f"   类别数: 6 (拳头/手掌/食指/胜利/点赞/OK)")
    
    # 初始化模型
    model = GestureNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)
    
    print("\n📌 第二步：开始训练")
    print("=" * 60)
    print(f"{'Epoch':>6} | {'Loss':>8} | {'Train Acc':>10} | {'Test Acc':>10} | {'Time':>8}")
    print("-" * 60)
    
    epochs = 200
    start_time = time.time()
    
    for epoch in range(epochs):
        # 训练
        model.train()
        optimizer.zero_grad()
        outputs = model(train_data)
        loss = criterion(outputs, train_labels)
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        if (epoch + 1) % 20 == 0:
            # 评估
            model.eval()
            with torch.no_grad():
                train_acc = (outputs.argmax(1) == train_labels).float().mean()
                test_outputs = model(test_data)
                test_loss = criterion(test_outputs, test_labels)
                test_acc = (test_outputs.argmax(1) == test_labels).float().mean()
            
            elapsed = time.time() - start_time
            print(f"{epoch+1:>6} | {loss.item():>8.4f} | "
                  f"{train_acc:>9.2%} | {test_acc:>9.2%} | "
                  f"{elapsed:>7.1f}s")
    
    total_time = time.time() - start_time
    print("=" * 60)
    print(f"训练完成！总耗时: {total_time:.1f}s ({epochs} epochs)")
    print()
    
    # 保存模型
    torch.save(model.state_dict(), "gesture_model.pth")
    print("✅ 模型已保存到 gesture_model.pth")
    
    return model


# ============================================
# 第五部分：推理性能测试
# ============================================

def benchmark(model):
    print("\n📌 第三步：推理性能测试")
    print("=" * 60)
    
    model.eval()
    
    # 模拟连续帧推理
    batch_sizes = [1, 10, 100, 1000]
    
    for batch_size in batch_sizes:
        # 生成模拟输入
        dummy_input = torch.randn(batch_size, 42).to(device)
        
        # 预热
        with torch.no_grad():
            _ = model(dummy_input)
        
        if device.type == 'mps':
            torch.mps.synchronize()
        
        # 正式计时
        n_runs = 100
        start = time.time()
        
        with torch.no_grad():
            for _ in range(n_runs):
                _ = model(dummy_input)
        
        if device.type == 'mps':
            torch.mps.synchronize()
        
        elapsed = time.time() - start
        avg_time = elapsed / n_runs
        fps = 1.0 / avg_time
        
        print(f"   批次大小 {batch_size:>4} | "
              f"平均推理时间: {avg_time*1000:>7.3f}ms | "
              f"FPS: {fps:>8.1f}")
    
    # 单帧推理延迟
    single_input = torch.randn(1, 42).to(device)
    
    with torch.no_grad():
        # 预热
        for _ in range(50):
            _ = model(single_input)
        
        if device.type == 'mps':
            torch.mps.synchronize()
        
        # 精确计时
        n_runs = 1000
        start = time.time()
        
        for _ in range(n_runs):
            _ = model(single_input)
        
        if device.type == 'mps':
            torch.mps.synchronize()
        
        elapsed = time.time() - start
        avg_latency = elapsed / n_runs
    
    print(f"\n   单帧推理延迟: {avg_latency*1000:.3f}ms")
    print(f"   理论最大 FPS: {1.0/avg_latency:.0f}")
    print()
    
    if avg_latency < 0.01:  # 10ms
        print("✅ 性能评估: 极佳 — 可支持 >100fps 的实时手势识别")
    elif avg_latency < 0.03:
        print("✅ 性能评估: 良好 — 可支持流畅的实时手势识别")
    elif avg_latency < 0.1:
        print("⚠️ 性能评估: 一般 — 可用于实时识别但可能有延迟")
    else:
        print("❌ 性能评估: 较差 — 不适合实时识别")


# ============================================
# 主程序
# ============================================

if __name__ == "__main__":
    # 训练模型
    model = train()
    
    # 性能测试
    benchmark(model)
    
    print("=" * 60)
    print("🎉 深度学习环境验证完成！")
    print("=" * 60)
    print()
    print("环境配置:")
    print(f"  - PyTorch: {torch.__version__}")
    print(f"  - 设备: {device}")
    print(f"  - 模型: GestureNet (42→128→64→6)")
    print(f"  - 训练数据: 模拟手势关键点数据")
    print()
    print("后续步骤:")
    print("  1. 打开系统偏好设置 → 隐私 → 摄像头 → 允许终端")
    print("  2. 重新运行本程序并选择实时识别模式")
    print("  3. 将模拟数据替换为真实摄像头数据")
