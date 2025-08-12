#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志查看和管理脚本
提供多种日志查看功能，包括实时监控、搜索、统计等
"""

import os
import sys
import time
import argparse
from datetime import datetime, timedelta
import re

def view_recent_logs(limit=50):
    """查看最近的日志记录"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        print(f"📊 日志文件总行数: {len(lines)}")
        print(f"📋 显示最近 {min(limit, len(lines))} 行日志:")
        print("=" * 80)
        
        # 显示最近的日志
        recent_lines = lines[-limit:] if len(lines) > limit else lines
        for line in recent_lines:
            print(line.rstrip())
            
    except Exception as e:
        print(f"❌ 读取日志文件失败: {e}")

def search_logs(keyword, case_sensitive=False):
    """搜索包含关键词的日志"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        # 搜索匹配的行
        matched_lines = []
        for i, line in enumerate(lines, 1):
            if case_sensitive:
                if keyword in line:
                    matched_lines.append((i, line))
            else:
                if keyword.lower() in line.lower():
                    matched_lines.append((i, line))
        
        if not matched_lines:
            print(f"🔍 未找到包含关键词 '{keyword}' 的日志")
            return
        
        print(f"🔍 找到 {len(matched_lines)} 条包含关键词 '{keyword}' 的日志:")
        print("=" * 80)
        
        for line_num, line in matched_lines:
            print(f"第{line_num}行: {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ 搜索日志失败: {e}")

def filter_logs_by_level(level):
    """按日志级别过滤日志"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        # 过滤指定级别的日志
        level_upper = level.upper()
        filtered_lines = []
        for i, line in enumerate(lines, 1):
            if f" - {level_upper} - " in line:
                filtered_lines.append((i, line))
        
        if not filtered_lines:
            print(f"🔍 未找到 {level_upper} 级别的日志")
            return
        
        print(f"🔍 找到 {len(filtered_lines)} 条 {level_upper} 级别的日志:")
        print("=" * 80)
        
        for line_num, line in filtered_lines:
            print(f"第{line_num}行: {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ 过滤日志失败: {e}")

def filter_logs_by_time(hours=24):
    """按时间过滤日志（最近N小时）"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        # 计算时间阈值
        threshold_time = datetime.now() - timedelta(hours=hours)
        filtered_lines = []
        
        for i, line in enumerate(lines, 1):
            try:
                # 解析日志时间
                time_str = line.split(' - ')[0]
                log_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S,%f')
                if log_time >= threshold_time:
                    filtered_lines.append((i, line))
            except:
                # 如果时间解析失败，跳过该行
                continue
        
        if not filtered_lines:
            print(f"🔍 最近 {hours} 小时内没有日志记录")
            return
        
        print(f"🔍 最近 {hours} 小时内的日志记录 ({len(filtered_lines)} 条):")
        print("=" * 80)
        
        for line_num, line in filtered_lines:
            print(f"第{line_num}行: {line.rstrip()}")
            
    except Exception as e:
        print(f"❌ 按时间过滤日志失败: {e}")

def get_log_statistics():
    """获取日志统计信息"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    try:
        with open('api.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("📝 日志文件为空")
            return
        
        # 统计信息
        total_lines = len(lines)
        info_count = 0
        warning_count = 0
        error_count = 0
        request_count = 0
        
        # 分析每行日志
        for line in lines:
            if " - INFO - " in line:
                info_count += 1
            elif " - WARNING - " in line:
                warning_count += 1
            elif " - ERROR - " in line:
                error_count += 1
            
            if "开始处理代码执行请求" in line:
                request_count += 1
        
        # 计算成功率
        success_count = 0
        for line in lines:
            if "请求处理完成" in line:
                success_count += 1
        
        success_rate = (success_count / request_count * 100) if request_count > 0 else 0
        
        print("📊 日志统计信息:")
        print("=" * 50)
        print(f"📝 总日志行数: {total_lines}")
        print(f"ℹ️  INFO级别: {info_count}")
        print(f"⚠️  WARNING级别: {warning_count}")
        print(f"❌ ERROR级别: {error_count}")
        print(f"🚀 总请求数: {request_count}")
        print(f"✅ 成功请求: {success_count}")
        print(f"📈 成功率: {success_rate:.1f}%")
        
        # 显示文件信息
        file_size = os.path.getsize('api.log')
        print(f"💾 日志文件大小: {file_size / 1024:.1f} KB")
        
        # 显示最近的请求
        recent_requests = []
        for line in reversed(lines):
            if "开始处理代码执行请求" in line:
                time_str = line.split(' - ')[0]
                recent_requests.append(time_str)
                if len(recent_requests) >= 5:
                    break
        
        if recent_requests:
            print(f"\n🕒 最近5次请求时间:")
            for req_time in recent_requests:
                print(f"   {req_time}")
                
    except Exception as e:
        print(f"❌ 获取日志统计失败: {e}")

def monitor_logs_realtime():
    """实时监控日志"""
    if not os.path.exists('api.log'):
        print("❌ 日志文件 api.log 不存在")
        return
    
    print("🔍 开始实时监控日志 (按 Ctrl+C 停止)...")
    print("=" * 80)
    
    try:
        # 获取当前文件大小
        current_size = os.path.getsize('api.log')
        
        while True:
            time.sleep(1)
            
            # 检查文件是否有新内容
            new_size = os.path.getsize('api.log')
            if new_size > current_size:
                # 读取新增的内容
                with open('api.log', 'r', encoding='utf-8') as f:
                    f.seek(current_size)
                    new_content = f.read()
                    if new_content.strip():
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {new_content.strip()}")
                
                current_size = new_size
                
    except KeyboardInterrupt:
        print("\n⏹️ 停止实时监控")

def clear_logs():
    """清空日志文件"""
    if not os.path.exists('api.log'):
        print("📝 日志文件不存在，无需清空")
        return
    
    try:
        # 备份当前日志
        backup_name = f"api_backup_{int(time.time())}.log"
        os.rename('api.log', backup_name)
        
        # 创建新的空日志文件
        with open('api.log', 'w', encoding='utf-8') as f:
            f.write(f"# 日志文件创建时间: {datetime.now()}\n")
        
        print(f"✅ 日志已清空，原日志备份为: {backup_name}")
        
    except Exception as e:
        print(f"❌ 清空日志失败: {e}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='日志查看和管理工具')
    parser.add_argument('action', choices=['view', 'search', 'level', 'time', 'stats', 'monitor', 'clear'], 
                       help='要执行的操作')
    parser.add_argument('--limit', '-l', type=int, default=50, help='显示的行数限制')
    parser.add_argument('--keyword', '-k', type=str, help='搜索关键词')
    parser.add_argument('--level', '-v', type=str, choices=['info', 'warning', 'error'], help='日志级别')
    parser.add_argument('--hours', '-t', type=int, default=24, help='时间范围（小时）')
    
    args = parser.parse_args()
    
    if args.action == 'view':
        view_recent_logs(args.limit)
    elif args.action == 'search':
        if not args.keyword:
            print("❌ 搜索操作需要指定关键词 (--keyword)")
            return
        search_logs(args.keyword)
    elif args.action == 'level':
        if not args.level:
            print("❌ 级别过滤需要指定日志级别 (--level)")
            return
        filter_logs_by_level(args.level)
    elif args.action == 'time':
        filter_logs_by_time(args.hours)
    elif args.action == 'stats':
        get_log_statistics()
    elif args.action == 'monitor':
        monitor_logs_realtime()
    elif args.action == 'clear':
        confirm = input("⚠️ 确定要清空所有日志吗？(y/N): ")
        if confirm.lower() == 'y':
            clear_logs()
        else:
            print("❌ 操作已取消")

if __name__ == "__main__":
    main()
