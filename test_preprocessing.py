#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 测试预处理逻辑
code_input = '''```python import matplotlib.pyplot as plt import matplotlib.font_manager as fm # 设置中文字体 font_path = fm.findfont(fm.FontProperties(family="SimHei")) plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name() # 区域轮廓坐标 x = [0, 1500, 1500, 0, 0] y = [0, 0, 4000, 1500, 0] # 主灯坐标 main_light_x = [750] main_light_y = [2000] # 绘制区域轮廓 plt.plot(x, y, label="区域轮廓") # 绘制主灯 plt.scatter(main_light_x, main_light_y, color="yellow", label="主灯", s=200) # 设置标题和标签 plt.title("option_1区域灯具点位布局") plt.xlabel("X 坐标 (mm)") plt.ylabel("Y 坐标 (mm)") # 显示图例 plt.legend() # 显示图形 plt.grid(True) plt.show() ```'''

print("原始代码:")
print(repr(code_input))

# 预处理代码，去除以```python开头和以```结尾的内容
code_to_execute = code_input
if code_to_execute.startswith('```python'):
    code_to_execute = code_to_execute[9:]  # 去除开头的```python
if code_to_execute.endswith('```'):
    code_to_execute = code_to_execute[:-3]  # 去除结尾的```

print("\n去除标记后的代码:")
print(repr(code_to_execute))

# 处理单行代码的情况，将分号分隔的代码拆分为多行
if ';' in code_to_execute and '\n' not in code_to_execute:
    code_to_execute = code_to_execute.replace('; ', '\n').replace(';', '\n')

print("\n处理分号后的代码:")
print(repr(code_to_execute))

# 处理单行中的多个import语句
if 'import ' in code_to_execute and code_to_execute.count('import ') > 1 and '\n' not in code_to_execute:
    # 将多个import语句分隔开
    import_parts = code_to_execute.split('import ')
    if import_parts[0] == '':
        import_parts = import_parts[1:]
    code_to_execute = '\n'.join([f'import {part}' for part in import_parts if part.strip()])

print("\n处理多个import后的代码:")
print(repr(code_to_execute))

# 修复缩进问题
lines = code_to_execute.split('\n')
# 移除空行和只包含空格的行
lines = [line for line in lines if line.strip()]
# 计算最小缩进
min_indent = float('inf')
for line in lines:
    if line.strip():
        indent = len(line) - len(line.lstrip())
        min_indent = min(min_indent, indent)
# 如果所有行都有缩进，则移除公共缩进
if min_indent != float('inf') and min_indent > 0:
    lines = [line[min_indent:] if len(line) >= min_indent else line for line in lines]
code_to_execute = '\n'.join(lines)

print("\n最终处理后的代码:")
print(code_to_execute)

# 尝试执行代码
try:
    exec(code_to_execute)
    print("\n代码执行成功！")
except Exception as e:
    print(f"\n代码执行失败: {e}")