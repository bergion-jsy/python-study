# 1. 导入库（Colab自带，无需安装）
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

# 2. 加载数据，这4行就是“处理数据”的起点
iris = load_iris()
X, y = iris.data, iris.target
# 只看前两类、前两个特征（为了你能画出图来）
X, y = X[y != 2, :2], y[y != 2]
# 把数据分成训练和测试
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
# 标准化——让梯度下降更稳定
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. 转成PyTorch认识的张量
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.long)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.long)

# 4. 定义一个最简单的神经网络（这就是“深度学习模型”）
class TinyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 10),   # 2个输入特征 -> 10个隐层神经元
            nn.ReLU(),
            nn.Linear(10, 2)    # 输出2个类别的得分
        )
    def forward(self, x):
        return self.net(x)

model = TinyNet()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# 5. 训练循环（这100个epoch就是“学习”的过程）
for epoch in range(100):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()
    if epoch % 20 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# 6. 测试
model.eval()
with torch.no_grad():
    _, preds = torch.max(model(X_test_t), 1)
    acc = (preds == y_test_t).sum().item() / len(y_test_t)
    print(f"Test Accuracy: {acc:.2f}")

# 7. 画出分类区域（你之前“划一条线”的自动化版本）
def plot_decision_boundary(model, X, y):
    x_min, x_max = X[:, 0].min()-1, X[:, 0].max()+1
    y_min, y_max = X[:, 1].min()-1, X[:, 1].max()+1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))
    grid = torch.tensor(np.c_[xx.ravel(), yy.ravel()], dtype=torch.float32)
    with torch.no_grad():
        Z = torch.argmax(model(grid), dim=1).numpy().reshape(xx.shape)
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k', cmap='coolwarm')
    plt.show()

plot_decision_boundary(model, X_test, y_test)
