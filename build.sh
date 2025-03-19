#!/usr/bin/env bash
# exit on error
set -o errexit

# 确保使用虚拟环境中的 Python
python3 -m venv venv
source venv/bin/activate

# 升级 pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 确保 gunicorn 安装在系统路径
pip install gunicorn --system
export PATH=$PATH:/opt/render/project/src/venv/bin

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 打印 gunicorn 位置（调试用）
which gunicorn