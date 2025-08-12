from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel
import io
import sys
import traceback
import io
import sys
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

# 强制设置字体，避免字体问题
import matplotlib.font_manager as fm
# 设置字体为系统默认
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

app = FastAPI(title="Python代码执行API", description="执行Python代码并返回生成的图片")

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
        
        # 创建安全的执行环境，预导入所有必要的库
        local_vars = {
            'plt': plt,
            'np': np,
            'Image': Image,
            'io': io,
            'base64': base64,
            'matplotlib': matplotlib,
            'sys': sys,
            'traceback': traceback
        }
        
        # 重定向标准输出和错误输出
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            # 执行代码，使用预配置的环境
            exec(request.code, {"__builtins__": {"__import__": __import__, "print": print, "len": len, "range": range, "list": list, "dict": dict, "str": str, "int": int, "float": float, "bool": bool, "exec": exec, "eval": eval}}, local_vars)
        
        # 记录代码执行完成
        logger.info(f"[{request_id}] Python代码执行完成")
        
        # 检查是否有matplotlib图形
        if plt.get_fignums():
            # 获取当前图形
            fig = plt.gcf()
            
            # 生成唯一的文件名
            import time
            import os
            timestamp = int(time.time())
            filename = f"output_{timestamp}.png"
            filepath = os.path.join("picture", filename)
            
            # 确保picture文件夹存在
            os.makedirs("picture", exist_ok=True)
            
            # 记录图片保存开始
            logger.info(f"[{request_id}] 开始保存图片到文件: {filepath}")
            
            # 将图形保存到文件
            fig.savefig(filepath, format='png', dpi=150, bbox_inches='tight')
            
            # 获取文件大小
            file_size = os.path.getsize(filepath)
            logger.info(f"[{request_id}] 图片保存成功: {filepath}, 大小: {file_size} 字节")
            
            # 同时保存到内存中的字节流用于返回
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
            img_buffer.seek(0)
            
            # 清理图形
            plt.close('all')
            
            # 计算总耗时
            total_time = time.time() - start_time
            logger.info(f"[{request_id}] 请求处理完成，总耗时: {total_time:.3f}秒")
            
            # 返回图片
            return Response(
                content=img_buffer.getvalue(),
                media_type="image/png",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )
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
            "/execute-code": "POST - 执行Python代码并返回图片",
            "/": "GET - 获取API信息"
        },
        "usage": "向/execute-code发送POST请求，包含Python代码，API将执行代码并返回生成的图片"
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

if __name__ == "__main__":
    import uvicorn
    logger.info("启动Python代码执行API服务")
    logger.info("服务地址: http://0.0.0.0:8000")
    logger.info("API文档: http://0.0.0.0:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
