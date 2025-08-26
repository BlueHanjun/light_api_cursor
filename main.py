from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response, FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io
import sys
import traceback
from contextlib import redirect_stdout, redirect_stderr
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import base64
import logging
import time
import json
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Python代码执行API", description="执行Python代码并返回生成的图片")

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    timeout: int = 30  # 执行超时时间（秒）

@app.post("/execute-code")
async def execute_code(request: CodeRequest):
    """
    执行Python代码并返回生成的图片
    
    参数:
    - code: 要执行的Python代码字符串
    - timeout: 执行超时时间（秒），默认30秒
    
    返回:
    - 图片数据（PNG格式）
    """
    # 记录请求开始
    start_time = time.time()
    request_id = f"req_{int(start_time * 1000)}"
    
    logger.info(f"[{request_id}] 开始处理代码执行请求")
    logger.info(f"[{request_id}] 请求参数: timeout={request.timeout}s, 代码长度={len(request.code)}字符")
    
    try:
        # 记录代码执行开始
        logger.info(f"[{request_id}] 开始执行Python代码")
        
        # 预处理代码，去除以```python开头和以```结尾的内容
        code_to_execute = request.code.strip()  # 先去除前后的空白字符
        if code_to_execute.startswith('```python'):
            code_to_execute = code_to_execute[9:]  # 去除开头的```python
        if code_to_execute.endswith('```'):
            code_to_execute = code_to_execute[:-3]  # 去除结尾的```
        code_to_execute = code_to_execute.strip()  # 再次去除前后的空白字符
        
        # 处理单行代码的情况，将分号分隔的代码拆分为多行
        if ';' in code_to_execute and '\n' not in code_to_execute:
            code_to_execute = code_to_execute.replace('; ', '\n').replace(';', '\n')
        
        # 处理单行中的多个import语句
        if 'import ' in code_to_execute and code_to_execute.count('import ') > 1 and '\n' not in code_to_execute:
            # 将多个import语句分隔开
            import_parts = code_to_execute.split('import ')
            if import_parts[0] == '':
                import_parts = import_parts[1:]
            code_to_execute = '\n'.join([f'import {part}' for part in import_parts if part.strip()])
        
        # 修复缩进问题
        import textwrap
        # 使用textwrap.dedent来处理缩进问题
        code_to_execute = textwrap.dedent(code_to_execute).strip()
        
        # 添加调试日志
        logger.info("缩进处理后的代码:")
        for i, line in enumerate(code_to_execute.split('\n')):
            logger.info(f"  {i+1}: {repr(line)}")
        
        # 替换plt.show()为plt.savefig()，确保在API环境中能够生成图片文件
        code_to_execute = code_to_execute.replace('plt.show()', 'plt.savefig("output.png")')
        
        logger.info(f"处理后的代码: {code_to_execute}")
        
        # 创建安全的执行环境，预导入所有必要的库
        local_vars = {
            'plt': plt,
            'np': np,
            'Image': Image,
            'io': io,
            'base64': base64,
            'matplotlib': matplotlib,
            'sys': sys,
            'traceback': traceback,
            'time': time
        }
        
        # 定义允许的内置函数
        allowed_builtins = {
            '__import__': __import__,
            'print': print,
            'len': len,
            'range': range,
            'list': list,
            'dict': dict,
            'str': str,
            'int': int,
            'float': float,
            'bool': bool,
            'exec': exec,
            'eval': eval,
            'enumerate': enumerate,
            'zip': zip,
            'map': map,
            'filter': filter,
            'sum': sum,
            'max': max,
            'min': min,
            'abs': abs,
            'round': round,
            'sorted': sorted,
            'reversed': reversed,
            'any': any,
            'all': all,
            'isinstance': isinstance,
            'hasattr': hasattr,
            'getattr': getattr,
            'setattr': setattr,
            'callable': callable,
            'open': open,
            'type': type,
            'issubclass': issubclass,
            'iter': iter,
            'next': next
        }
        
        # 重定向标准输出和错误输出
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        # 记录执行前的图形数量
        logger.info(f"[{request_id}] 执行前 plt.get_fignums(): {plt.get_fignums()}")
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            # 执行代码，使用预配置的环境
            exec(code_to_execute, {"__builtins__": allowed_builtins}, local_vars)
        
        # 记录代码执行完成
        logger.info(f"[{request_id}] Python代码执行完成")
        
        # 记录执行后的图形数量
        logger.info(f"[{request_id}] 执行后 plt.get_fignums(): {plt.get_fignums()}")
        
        # 检查是否有matplotlib图形
        if plt.get_fignums():
            # 获取当前图形
            fig = plt.gcf()
            
            # 保存图片到临时文件
            fig.savefig("output.png")
            
            # 生成唯一的文件名
            import os
            timestamp = int(time.time())
            filename = f"output_{timestamp}.png"
            filepath = os.path.join("picture", filename)
            
            # 确保picture文件夹存在
            import os
            if not os.path.exists("picture"):
                os.makedirs("picture")
            logger.info(f"[{request_id}] picture文件夹路径: {os.path.abspath('picture')}")
            
            # 记录图片保存开始
            logger.info(f"[{request_id}] 开始保存图片到文件: {filepath}")
            
            # 将图形保存到文件
            fig.savefig(filepath, format='png', dpi=150, bbox_inches='tight')
            
            # 确保文件写入完成
            import os
            with open(filepath, 'r') as f:
                os.fsync(f.fileno())
            
            # 获取文件大小
            file_size = os.path.getsize(filepath)
            logger.info(f"[{request_id}] 图片保存成功: {filepath}, 大小: {file_size} 字节")
            
            # 同时保存到内存中的字节流用于返回
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            # 获取图片的base64编码
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
            # 清理图形
            plt.close('all')
            
            # 计算总耗时
            total_time = time.time() - start_time
            logger.info(f"[{request_id}] 请求处理完成，总耗时: {total_time:.3f}秒")
            
            # 返回图片下载链接和图片二进制数据的base64编码
            # download_url = f"http://localhost:8000/download/{filename}"
            # 部署阿里云时用这个 好难
            download_url = f"http://114.55.226.87:8000/download/{filename}" 
            return {"download_url": download_url, "image_data": img_base64}
        else:
            # 如果没有生成图片，记录警告并返回错误信息
            logger.warning(f"[{request_id}] 代码执行成功但未生成图片")
            raise HTTPException(
                status_code=400, 
                detail="代码执行成功但未生成图片。请确保代码中包含matplotlib绘图代码。"
            )
            
    except Exception as e:
        # 记录错误信息
        error_msg = f"代码执行失败: {str(e)}"
        logger.error(f"[{request_id}] {error_msg}")
        logger.error(f"[{request_id}] 错误详情: {traceback.format_exc()}")
        
        # 计算总耗时
        total_time = time.time() - start_time
        logger.error(f"[{request_id}] 请求处理失败，总耗时: {total_time:.3f}秒")
        
        # 返回详细的错误信息
        error_msg = f"代码执行失败: {str(e)}\n\n错误详情:\n{traceback.format_exc()}"
        raise HTTPException(status_code=400, detail=error_msg)

@app.get("/")
async def root():
    """API根路径，返回使用说明"""
    logger.info("访问API根路径")
    return {
        "message": "Python代码执行API",
        "endpoints": {
            "/execute-code": "POST - 执行Python代码并返回图片下载链接",
            "/download/{filename}": "GET - 下载生成的图片",
            "/": "GET - 获取API信息"
        },
        "usage": "向/execute-code发送POST请求，包含Python代码，API将执行代码并返回生成的图片下载链接"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    logger.info("健康检查请求")
    return {"status": "healthy", "message": "API运行正常"}

@app.get("/logs")
async def get_logs(limit: int = 100):
    """获取最近的日志记录"""
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 返回最近的日志记录
            recent_logs = lines[-limit:] if len(lines) > limit else lines
            return {
                "total_lines": len(lines),
                "returned_lines": len(recent_logs),
                "logs": recent_logs
            }
    except FileNotFoundError:
        return {"error": "日志文件不存在"}
    except Exception as e:
        logger.error(f"读取日志文件失败: {str(e)}")
        return {"error": f"读取日志失败: {str(e)}"}

@app.get("/download/{filename}")
async def download_image(filename: str):
    """
    下载生成的图片
    
    参数:
    - filename: 图片文件名
    
    返回:
    - 图片文件
    """
    import os
    filepath = os.path.join("picture", filename)
    
    # 检查文件是否存在
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="图片文件不存在")
    
    # 返回文件
    return FileResponse(filepath, media_type="image/png", filename=filename)


if __name__ == "__main__":
    import uvicorn
    logger.info("启动Python代码执行API服务")
    logger.info("服务地址: http://0.0.0.0:8000")
    logger.info("API文档: http://0.0.0.0:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
