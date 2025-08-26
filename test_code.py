import requests
import json
import base64

code = '''import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 设置中文字体
font_path = 'SimHei.ttf'
font = FontProperties(fname=font_path)

# 房间轮廓坐标
room_coords = [(0, 0), (1500, 0), (1500, 4000), (0, 4000), (0, 0)]
x_room, y_room = zip(*room_coords)

# 灯具坐标
spotlights = [(750, 600), (750, 2100), (750, 3600), (750, 3900)]
x_spot, y_spot = zip(*spotlights)

# 家具信息（挂画）
painting_x = [0, 1500]
painting_y = [3900, 3900]

# 创建画布
fig, ax = plt.subplots(1, 2, figsize=(12, 6))

# 绘制房间轮廓
ax[0].plot(x_room, y_room, 'k-')

# 绘制灯具
ax[0].scatter(x_spot, y_spot, c='r', label='Spotlight')

# 绘制挂画
ax[0].plot(painting_x, painting_y, 'b--', label='Painting')

# 设置坐标轴标签和标题
ax[0].set_xlabel('East (mm)', fontproperties=font)
ax[0].set_ylabel('North (mm)', fontproperties=font)
ax[0].set_title('Corridor Lighting Layout', fontproperties=font)

# 设置坐标轴比例
ax[0].set_aspect('equal')

# 绘制图例
legend_elements = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Spotlight'),
    plt.Line2D([0], [0], linestyle='--', color='b', label='Painting')
]
ax[1].legend(handles=legend_elements, loc='center', prop=font)
ax[1].axis('off')

plt.savefig("output.png")'''

url = "http://localhost:8000/execute-code"
headers = {"Content-Type": "application/json"}
data = {"code": code, "timeout": 30}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print("请求成功:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 保存返回的图片数据到文件
    if 'image_data' in result:
        image_data = base64.b64decode(result['image_data'])
        with open('returned_image.png', 'wb') as f:
            f.write(image_data)
        print("图片已保存为 returned_image.png")
    else:
        print("响应中没有图片数据")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(response.text)