import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 创建简单图形
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.title('Simple Plot')
plt.xlabel('X')
plt.ylabel('Y')

# 显示图形
plt.show()