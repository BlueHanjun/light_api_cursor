#!/bin/bash

# Python代码执行API启动脚本

echo "🚀 启动Python代码执行API服务..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到pip3，请先安装pip3"
    exit 1
fi

# 安装依赖
echo "📦 安装项目依赖..."
pip3 install -r requirements.txt

# 启动服务
echo "🌐 启动FastAPI服务..."
echo "📍 服务地址: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "🔧 按 Ctrl+C 停止服务"

python3 main.py
