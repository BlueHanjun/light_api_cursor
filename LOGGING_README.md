# 日志系统使用说明

本文档介绍Python代码执行API的日志系统功能和使用方法。

## 🚀 功能特性

### 1. 自动日志记录
- **请求日志**: 记录每个API请求的详细信息
- **执行日志**: 记录代码执行的各个阶段
- **错误日志**: 记录详细的错误信息和堆栈跟踪
- **性能日志**: 记录请求处理时间和资源使用情况

### 2. 日志级别
- **INFO**: 一般信息（默认）
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **DEBUG**: 调试信息（开发环境）

### 3. 日志格式
```
时间戳 - 模块名 - 日志级别 - 消息内容
例如: 2024-08-12 10:00:00,123 - __main__ - INFO - 开始处理代码执行请求
```

## 📁 日志文件

### 主要日志文件
- **`api.log`**: 主要的API日志文件
- **`requests.log`**: 请求专用日志（可选）
- **`errors.log`**: 错误专用日志（可选）

### 日志轮转
- 自动轮转：单个日志文件超过10MB时自动创建新文件
- 备份保留：保留最近5个备份文件
- 自动清理：可配置自动清理30天前的旧日志

## 🛠️ 使用方法

### 1. 查看日志

#### 查看最近的日志
```bash
python3 view_logs.py view
python3 view_logs.py view --limit 100
```

#### 搜索特定关键词
```bash
python3 view_logs.py search --keyword "错误"
python3 view_logs.py search --keyword "req_"
```

#### 按日志级别过滤
```bash
python3 view_logs.py level --level error
python3 view_logs.py level --level warning
```

#### 按时间过滤
```bash
python3 view_logs.py time --hours 24
python3 view_logs.py time --hours 168  # 一周
```

#### 获取统计信息
```bash
python3 view_logs.py stats
```

#### 实时监控日志
```bash
python3 view_logs.py monitor
```

#### 清空日志
```bash
python3 view_logs.py clear
```

### 2. 通过API查看日志

#### 获取最近的日志
```bash
curl http://localhost:8000/logs
curl "http://localhost:8000/logs?limit=50"
```

### 3. 日志配置

#### 基本配置
```python
from logging_config import setup_logging

# 设置基本日志
logger = setup_logging(
    log_file='api.log',
    log_level=logging.INFO,
    max_bytes=10*1024*1024,  # 10MB
    backup_count=5,
    console_output=True
)
```

#### 专用日志记录器
```python
from logging_config import setup_request_logging, setup_error_logging

# 设置请求日志
request_logger = setup_request_logging()

# 设置错误日志
error_logger = setup_error_logging()
```

## 📊 日志内容示例

### 成功的请求日志
```
2024-08-12 10:00:00,123 - __main__ - INFO - [req_1754963888000] 开始处理代码执行请求
2024-08-12 10:00:00,124 - __main__ - INFO - [req_1754963888000] 请求参数: timeout=30s, 代码长度=500字符
2024-08-12 10:00:00,125 - __main__ - INFO - [req_1754963888000] 开始执行Python代码
2024-08-12 10:00:00,130 - __main__ - INFO - [req_1754963888000] Python代码执行完成
2024-08-12 10:00:00,131 - __main__ - INFO - [req_1754963888000] 开始保存图片到文件: picture/output_1754963888.png
2024-08-12 10:00:00,135 - __main__ - INFO - [req_1754963888000] 图片保存成功: picture/output_1754963888.png, 大小: 41729 字节
2024-08-12 10:00:00,136 - __main__ - INFO - [req_1754963888000] 请求处理完成，总耗时: 0.013秒
```

### 错误的请求日志
```
2024-08-12 10:01:00,123 - __main__ - INFO - [req_1754963889000] 开始处理代码执行请求
2024-08-12 10:01:00,124 - __main__ - INFO - [req_1754963889000] 请求参数: timeout=30s, 代码长度=200字符
2024-08-12 10:01:00,125 - __main__ - INFO - [req_1754963889000] 开始执行Python代码
2024-08-12 10:01:00,126 - __main__ - ERROR - [req_1754963889000] 代码执行失败: name 'undefined_variable' is not defined
2024-08-12 10:01:00,127 - __main__ - ERROR - [req_1754963889000] 错误详情: Traceback (most recent call last):...
2024-08-12 10:01:00,128 - __main__ - ERROR - [req_1754963889000] 请求处理失败，总耗时: 0.005秒
```

## 🔧 配置选项

### 环境变量配置
```bash
# 日志级别
export LOG_LEVEL=INFO

# 日志文件路径
export LOG_FILE=api.log

# 最大文件大小（MB）
export LOG_MAX_SIZE=10

# 备份文件数量
export LOG_BACKUP_COUNT=5
```

### 配置文件
可以创建 `logging.conf` 文件来自定义日志配置：

```ini
[loggers]
keys=root,api,request,error

[handlers]
keys=consoleHandler,fileHandler,requestHandler,errorHandler

[formatters]
keys=defaultFormatter,requestFormatter,errorFormatter

[logger_root]
level=INFO
handlers=consoleHandler,fileHandler

[logger_api]
level=INFO
handlers=fileHandler
qualname=__main__

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=defaultFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=handlers.RotatingFileHandler
level=INFO
formatter=defaultFormatter
args=('api.log', 'a', 10485760, 5, 'utf-8')

[formatter_defaultFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

## 📈 性能监控

### 请求处理时间
每个请求都会记录处理时间，帮助识别性能瓶颈：

```
总耗时: 0.013秒
```

### 资源使用情况
- 图片文件大小
- 内存使用情况
- 执行时间分布

## 🚨 故障排除

### 常见问题

#### 1. 日志文件过大
```bash
# 手动清理旧日志
python3 view_logs.py clear

# 或者删除旧的备份文件
rm api.log.*
```

#### 2. 日志权限问题
```bash
# 检查文件权限
ls -la *.log

# 修复权限
chmod 644 *.log
```

#### 3. 磁盘空间不足
```bash
# 检查磁盘空间
df -h

# 清理旧日志
python3 logging_config.py cleanup_old_logs
```

### 日志分析技巧

#### 1. 查找错误模式
```bash
# 搜索所有错误
python3 view_logs.py level --level error

# 搜索特定错误类型
python3 view_logs.py search --keyword "ModuleNotFoundError"
```

#### 2. 性能分析
```bash
# 查找慢请求
python3 view_logs.py search --keyword "总耗时: 1."

# 统计成功率
python3 view_logs.py stats
```

#### 3. 请求追踪
```bash
# 追踪特定请求
python3 view_logs.py search --keyword "req_1754963888000"
```

## 🔮 未来功能

- [ ] 日志聚合和分析
- [ ] 实时告警系统
- [ ] 日志可视化界面
- [ ] 自动性能报告
- [ ] 日志压缩和归档

## 📞 技术支持

如果您在使用日志系统时遇到问题，请：

1. 检查日志文件是否存在
2. 查看错误日志中的详细信息
3. 使用 `python3 view_logs.py stats` 检查系统状态
4. 联系开发团队并提供相关日志信息
