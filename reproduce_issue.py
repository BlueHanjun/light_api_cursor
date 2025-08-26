import requests
import json

# 模拟用户可能发送的代码（包含可能的格式问题）
code_with_formatting = '''```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 设置中文字体
font_path = fm.findfont(fm.FontProperties(family="SimHei"))
plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()

# 区域轮廓坐标
x = [0, 1500, 1500, 0, 0]
y = [0, 0, 4000, 1500, 0]

# 主灯坐标
main_light_x = [750]
main_light_y = [2000]

# 绘制区域轮廓
plt.plot(x, y, label="区域轮廓")

# 绘制主灯
plt.scatter(main_light_x, main_light_y, color="yellow", label="主灯", s=200)

# 设置标题和标签
plt.title("option_1区域灯具点位布局")
plt.xlabel("X 坐标 (mm)")
plt.ylabel("Y 坐标 (mm)")

# 显示图例
plt.legend()

# 显示图形
plt.grid(True)
plt.show()
```'''

# 发送请求到API
response = requests.post('http://localhost:8000/execute-code', json={'code': code_with_formatting})

# 打印响应
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# 如果有错误，尝试获取更多日志信息
if response.status_code != 200:
    try:
        # 获取最近的日志
        log_response = requests.get('http://localhost:8000/logs?limit=10')
        if log_response.status_code == 200:
            logs = log_response.json()
            print("Recent logs:")
            for log in logs.get('logs', []):
                print(log.strip())
    except Exception as e:
        print(f"Failed to get logs: {e}")