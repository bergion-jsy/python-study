import numpy as np
import matplotlib.pyplot as plt

# 定义行空间和零空间的方向
row_dir = np.array([1, 1])   # 行空间基向量
null_dir = np.array([1, -1]) # 零空间基向量

# 参数范围
t = np.linspace(-3, 3, 100)

# 行空间直线: beta = t * row_dir
row_line = np.outer(row_dir, t).T

# 零空间直线: beta = s * null_dir
null_line = np.outer(null_dir, t).T

# 选一个特解 beta0
beta0 = np.array([2, 0])

# 解集: beta0 + s * null_dir
s_vals = np.linspace(-3, 3, 100)
sol_set = beta0 + np.outer(null_dir, s_vals).T

# 可估函数: c = (1,1), 等值线 c^T beta = constant
# 在二维平面上画几条等值线
c = np.array([1, 1])
const_vals = [-2, 0, 2, 4, 6]
x_vals = np.linspace(-3, 5, 200)
for const in const_vals:
    # 直线方程: beta1 + beta2 = const  => beta2 = const - beta1
    y_vals = const - x_vals
    plt.plot(x_vals, y_vals, 'g--', alpha=0.5, linewidth=1)

# 不可估函数: d = (1,-1), 等值线 (仅画一条示意)
d = np.array([1, -1])
# 在解集上，d^T beta 会变化，画一条过 beta0 的等值线 (d^T beta = d^T beta0)
const_d = d @ beta0
x_vals_d = np.linspace(-1, 5, 200)
y_vals_d = (const_d - d[0]*x_vals_d) / d[1]
plt.plot(x_vals_d, y_vals_d, 'r:', linewidth=1.5, label=r'$d^T\beta = \text{const}$ (not estimable)')

# 绘制
plt.plot(row_line[:,0], row_line[:,1], 'b-', linewidth=2, label=r'$\mathrm{Row}(X)$')
plt.plot(null_line[:,0], null_line[:,1], 'k--', linewidth=1.5, label=r'$\mathrm{Null}(X)$')
plt.plot(sol_set[:,0], sol_set[:,1], 'r-', linewidth=2, label='Least squares solution set')
plt.plot(beta0[0], beta0[1], 'ro', markersize=6, label=r'$\beta_0$ (a particular solution)')

# 标记可估函数等值线的例子
plt.text(3, -1, r'$c^T\beta = \mathrm{const}$', color='green', fontsize=10,
         bbox=dict(facecolor='white', alpha=0.5))

# 图例与坐标轴
plt.axhline(0, color='gray', linewidth=0.5)
plt.axvline(0, color='gray', linewidth=0.5)
plt.grid(True, linestyle=':', alpha=0.6)
plt.xlabel(r'$\beta_1$')
plt.ylabel(r'$\beta_2$')
plt.title('Parameter space decomposition when $X$ is column-rank deficient')
plt.legend(loc='upper left')
plt.axis('equal')
plt.xlim(-3, 5)
plt.ylim(-3, 3)
plt.show()