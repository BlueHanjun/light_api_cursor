# Python代码执行API

这是一个基于FastAPI的后端服务，可以执行Python代码并返回生成的图片。

## 功能特性

- 执行Python代码字符串
- 支持matplotlib、numpy等科学计算库
- 自动捕获代码执行结果
- 返回PNG格式的图片
- 安全的代码执行环境
- 详细的错误处理和反馈

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python main.py
```

或者使用uvicorn：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API接口

### 1. 执行代码接口

**POST** `/execute-code`

**请求体：**
```json
{
    "code": "你的Python代码字符串",
    "timeout": 30
}
```

**响应：**
- 成功：返回PNG格式的图片
- 失败：返回错误信息

### 2. 健康检查

**GET** `/health`

### 3. API信息

**GET** `/`

## 使用示例

### 生成简单图表

```python
import requests

code = """
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('正弦函数图')
plt.xlabel('x')
plt.ylabel('sin(x)')
plt.grid(True)
plt.show()
"""

response = requests.post(
    "http://localhost:8000/execute-code",
    json={"code": code}
)

if response.status_code == 200:
    with open("output.png", "wb") as f:
        f.write(response.content)
    print("图片已保存为 output.png")
else:
    print("错误:", response.json())
```

### 生成数据可视化

```python
code = """
import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据
np.random.seed(42)
data = np.random.randn(1000)

plt.figure(figsize=(12, 8))

# 创建子图
plt.subplot(2, 2, 1)
plt.hist(data, bins=30, alpha=0.7, color='skyblue')
plt.title('直方图')
plt.xlabel('值')
plt.ylabel('频次')

plt.subplot(2, 2, 2)
plt.scatter(np.arange(len(data)), data, alpha=0.5, s=20)
plt.title('散点图')
plt.xlabel('索引')
plt.ylabel('值')

plt.subplot(2, 2, 3)
plt.boxplot(data)
plt.title('箱线图')
plt.ylabel('值')

plt.subplot(2, 2, 4)
plt.plot(np.cumsum(data), 'g-', linewidth=1)
plt.title('累积和')
plt.xlabel('索引')
plt.ylabel('累积值')

plt.tight_layout()
plt.show()
"""
```

## 注意事项

1. **代码安全**：API在受限环境中执行代码，但仍需注意安全
2. **图片生成**：确保代码中包含matplotlib绘图代码
3. **超时设置**：默认30秒超时，可根据需要调整
4. **内存管理**：执行完成后会自动清理matplotlib图形
5. **中文字体支持**：API默认支持Heiti TC、Hiragino Sans、PingFang SC等中文字体，可在代码中设置使用中文标签和标题

## 支持的科学计算库

- matplotlib：图表绘制
- numpy：数值计算
- PIL/Pillow：图像处理
- seaborn：统计图表
- plotly：交互式图表

## 开发环境

- Python 3.8+
- FastAPI 0.104.1+
- uvicorn
- matplotlib
- numpy
- Pillow
