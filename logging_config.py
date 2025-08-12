#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志配置文件
提供灵活的日志配置选项，包括文件轮转、格式化等
"""

import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(
    log_file='api.log',
    log_level=logging.INFO,
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5,
    console_output=True
):
    """
    设置日志配置
    
    参数:
    - log_file: 日志文件名
    - log_level: 日志级别
    - max_bytes: 单个日志文件最大大小
    - backup_count: 保留的备份文件数量
    - console_output: 是否同时输出到控制台
    """
    
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 清除现有的handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器（带轮转）
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 控制台处理器（可选）
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 记录启动信息
    logger.info(f"日志系统初始化完成")
    logger.info(f"日志文件: {log_file}")
    logger.info(f"日志级别: {logging.getLevelName(log_level)}")
    logger.info(f"最大文件大小: {max_bytes / (1024*1024):.1f} MB")
    logger.info(f"备份文件数量: {backup_count}")
    
    return logger

def setup_request_logging():
    """设置请求专用的日志记录器"""
    request_logger = logging.getLogger('request')
    request_logger.setLevel(logging.INFO)
    
    # 创建请求日志文件
    request_log_file = 'requests.log'
    
    # 请求日志处理器
    request_handler = logging.handlers.RotatingFileHandler(
        request_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    
    # 请求日志格式化器
    request_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    request_handler.setFormatter(request_formatter)
    request_logger.addHandler(request_handler)
    
    return request_logger

def setup_error_logging():
    """设置错误专用的日志记录器"""
    error_logger = logging.getLogger('error')
    error_logger.setLevel(logging.ERROR)
    
    # 创建错误日志文件
    error_log_file = 'errors.log'
    
    # 错误日志处理器
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    
    # 错误日志格式化器
    error_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s\n'
        'Traceback: %(exc_info)s\n'
        '='*80,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    error_handler.setFormatter(error_formatter)
    error_logger.addHandler(error_handler)
    
    return error_logger

def get_log_file_info(log_file='api.log'):
    """获取日志文件信息"""
    if not os.path.exists(log_file):
        return None
    
    try:
        stat = os.stat(log_file)
        size_kb = stat.st_size / 1024
        
        return {
            'file_path': log_file,
            'size_kb': size_kb,
            'size_mb': size_kb / 1024,
            'modified_time': datetime.fromtimestamp(stat.st_mtime),
            'created_time': datetime.fromtimestamp(stat.st_ctime)
        }
    except Exception as e:
        return {'error': str(e)}

def cleanup_old_logs(log_dir='.', days_to_keep=30):
    """清理旧的日志文件"""
    import glob
    from datetime import datetime, timedelta
    
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    cleaned_files = []
    
    # 查找所有日志文件
    log_patterns = ['*.log', '*.log.*']
    
    for pattern in log_patterns:
        for log_file in glob.glob(os.path.join(log_dir, pattern)):
            try:
                file_time = datetime.fromtimestamp(os.path.getctime(log_file))
                if file_time < cutoff_date:
                    os.remove(log_file)
                    cleaned_files.append(log_file)
            except Exception as e:
                print(f"清理文件 {log_file} 失败: {e}")
    
    return cleaned_files

if __name__ == "__main__":
    # 测试日志配置
    print("🧪 测试日志配置...")
    
    # 设置日志
    logger = setup_logging()
    
    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    
    # 获取日志文件信息
    info = get_log_file_info()
    if info:
        print(f"📊 日志文件信息: {info}")
    
    print("✅ 日志配置测试完成")
