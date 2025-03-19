#!/usr/bin/env bash
# exit on error
set -o errexit

# Python虚拟环境命令
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移命令
python manage.py makemigrations
python manage.py migrate

# 收集静态文件（如果需要）
python manage.py collectstatic --noinput