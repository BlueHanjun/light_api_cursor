#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取特定请求的详细信息
"""

import os
import sys
import re

def get_request_details(request_id):
    """获取特定请求的详细信息"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        # 查找请求的相关日志
        request_lines = []
        for line in lines:
            if f"[{request_id}]" in line:
                request_lines.append(line.rstrip())
        
        if not request_lines:
            print(f"🔍 未找到请求ID为 '{request_id}' 的日志")
            return
        
        print(f"🔍 找到 {len(request_lines)} 条与请求 '{request_id}' 相关的日志:")
        print("=" * 80)
        
        for line in request_lines:
            print(line)
        
        # 尝试提取代码内容（如果有的话）
        # 这需要在API中添加额外的日志记录
        
    except Exception as e:
        print(f"❌ 获取请求详情失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python3 get_request_details.py <request_id>")
        sys.exit(1)
    
    request_id = sys.argv[1]
    get_request_details(request_id)