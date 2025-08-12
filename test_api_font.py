import matplotlib
matplotlib.use('Agg')  # 设置matplotlib后端
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制区域轮廓（简化示例）
area_points = np.array([[0, 0], [10, 0], [10, 8], [0, 8], [0, 0]])
ax.plot(area_points[:, 0], area_points[:, 1], 'b-', linewidth=2, label='区域轮廓')

# 绘制灯具点位
light_positions = [
    (2, 2), (8, 2), (5, 6),  # 主灯
    (3, 4), (7, 4),          # 辅助灯
]

for i, (x, y) in enumerate(light_positions):
    if i < 3:  # 主灯
        ax.plot(x, y, 'ro', markersize=10, label='主灯' if i == 0 else "")
    else:  # 辅助灯
        ax.plot(x, y, 'yo', markersize=8, label='辅助灯' if i == 3 else "")

# 设置图形属性
ax.set_xlim(-1, 11)
ax.set_ylim(-1, 9)
ax.set_xlabel('X坐标')
ax.set_ylabel('Y坐标')
ax.set_title('区域灯具点位布局图')
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# 显示图形
plt.show()