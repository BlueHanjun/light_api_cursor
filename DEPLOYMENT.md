# 部署到阿里云服务器指南

本文档将指导您如何将Python代码执行API部署到阿里云服务器上。

## 前提条件

1. 您已经拥有一台阿里云ECS服务器
2. 服务器操作系统为Linux（推荐Ubuntu 20.04或CentOS 8）
3. 服务器已配置好SSH访问
4. 服务器已开放8000端口（或您指定的其他端口）

## 部署步骤

### 1. 连接到阿里云服务器

使用SSH连接到您的阿里云服务器：

```bash
ssh root@your_server_ip
```

### 2. 更新系统包

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

### 3. 安装Python3和pip

```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip -y

# CentOS/RHEL
sudo yum install python3 python3-pip -y
```

### 4. 上传项目文件

您可以通过多种方式将项目文件上传到服务器，以下是一种推荐方式：

#### 使用SCP命令上传（在本地执行）

```bash
# 在本地终端执行
scp -r /path/to/light_api_cursor root@your_server_ip:/root/
```

或者您可以直接在服务器上克隆项目（如果项目已托管在Git仓库中）：

```bash
# 在服务器上执行
git clone your_repository_url
```

### 5. 安装项目依赖

```bash
# 进入项目目录
cd light_api_cursor

# 安装依赖
    pip3 install -r requirements.txt
```

### 6. 启动服务

您可以直接运行启动脚本：

```bash
chmod +x start_server.sh
./start_server.sh
```

或者直接运行主程序：

```bash
python3 main.py
```

### 7. 后台运行服务（可选）

为了确保服务在SSH断开后仍能继续运行，您可以使用以下方法之一：

#### 使用nohup

```bash
nohup python3 main.py > app.log 2>&1 &
```

#### 使用screen（推荐）

```bash
# 安装screen
sudo apt install screen -y  # Ubuntu/Debian
# 或
sudo yum install screen -y   # CentOS/RHEL

# 创建新的screen会话
screen -S python-api

# 在screen会话中运行服务
python3 main.py

# 按Ctrl+A，然后按D键分离会话
# 要重新连接会话，使用：screen -r python-api
```

### 8. 配置防火墙

确保服务器防火墙允许8000端口的流量：

```bash
# Ubuntu/Debian (UFW)
sudo ufw allow 8000

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### 9. 访问API

服务启动后，您可以通过以下地址访问API：

```
http://your_server_ip:8000
```

API文档地址：

```
http://your_server_ip:8000/docs
```

## 生产环境建议

1. 使用Nginx作为反向代理
2. 使用Gunicorn作为WSGI服务器
3. 配置SSL证书以启用HTTPS
4. 设置环境变量管理敏感配置
5. 使用systemd管理服务进程

### 使用Gunicorn和Nginx部署（推荐）

1. 安装Gunicorn：

```bash
pip3 install gunicorn
```

2. 使用Gunicorn启动应用：

```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

3. 配置Nginx反向代理（创建`/etc/nginx/sites-available/python-api`）：

```nginx
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

4. 启用Nginx配置：

```bash
sudo ln -s /etc/nginx/sites-available/python-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 故障排除

1. 如果服务无法启动，请检查端口是否被占用：

```bash
lsof -i :8000
```

2. 查看应用日志：

```bash
tail -f app.log
```

3. 检查防火墙设置是否正确

4. 确保所有依赖都已正确安装