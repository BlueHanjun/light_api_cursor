"""
测试中文字体支持功能
"""

import requests
import base64

def test_chinese_font_support():
    # 测试包含中文字体设置的代码
    code = '''
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 创建数据
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 绘制图形
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title("中文标题测试")
plt.xlabel("X轴标签")
plt.ylabel("Y轴标签")
plt.grid(True)
'''
    
    # 发送请求到API
    url = "http://localhost:8000/execute-code"
    payload = {
        "code": code,
        "timeout": 30
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        # 保存图片
        with open("test_chinese_font_result.png", "wb") as f:
            f.write(response.content)
        print("测试成功！图片已保存为 test_chinese_font_result.png")
        print(f"图片大小: {len(response.content)} 字节")
    else:
        print(f"测试失败！状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    test_chinese_font_support()