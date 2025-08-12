import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = fm.findfont(fm.FontProperties(family='SimHei'))
plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()

# 区域轮廓坐标
x = [0, 1500, 1500, 0, 0]
y = [0, 0, 4000, 1500, 0]

# 主灯坐标
main_light_x = [750]
main_light_y = [2000]

# 绘制区域轮廓
plt.plot(x, y, label='区域轮廓')

# 绘制主灯
plt.scatter(main_light_x, main_light_y, color='yellow', label='主灯', s=200)

# 设置标题和标签
plt.title('option_1区域灯具点位布局')
plt.xlabel('X 坐标 (mm)')
plt.ylabel('Y 坐标 (mm)')

# 显示图例
plt.legend()

# 显示图形
plt.grid(True)
plt.show()