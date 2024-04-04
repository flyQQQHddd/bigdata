# 环境配置

## 使用 VSCode 登录服务器

使用 vscode 的 ssh 插件远程登录服务器

## 配置MiniConda

```
# 下载 miniconda 安装包
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh
# 安装 miniconda 
bash Miniconda3-py39_24.1.2-0-Linux-x86_64.sh
# 初始化 miniconda
source ~/.bashrc
```

## 配置Python以及Django

```
# 创建 python 虚拟环境
conda create --name bigdata python=3.10
# 激活 python 虚拟环境
conda activate bigdata
# 安装 python django 库，使用镜像源
pip install django -i https://mirrors.aliyun.com/pypi/simple/
```

## 创建并启动Django项目

```
# 新建名为 bigdata 的 django 项目
django-admin startproject bigdata
# 进入 django 项目
cd bigdata
# 进入开发模式，vscode 会将服务器端口转发到本地
python manage.py runserver
```

## 基础配置

以下操作均在`setting.py`中进行

1. 配置模板文件路径
   ```
   TEMPLATES  =  [
   	...
   	'DIRS': [os.path.join(BASE_DIR, 'templates')]
   	...
   	]
   ```

2. 设置允许的IP
   ```
   ALLOWED_HOSTS = ["47.116.207.105"]
   ```
3. 配置全局静态文件目录
   ```
   STATICFILES_DIRS = [
      os.path.join(BASE_DIR, 'static')
   ]
   ```

## 服务器后台运行服务

```
# 安装 tmux 程序
sudo apt install tmux
# 创建名为 bigdataserver 的会话
tmux new -s bigdataserver
# 在会话中激活 python 环境并进入 django 开发模式，指定所有IP可访问
conda activate bigdata
python manage.py runserver 0.0.0.0:8080

# 退出会话，之后再退出命令行，django 服务不会中止
ctrl + b d

# 查看 tmux 会话列表
tmux ls 
# 重连名为 bigdataserver 的会话
tmux a -t bigdataserver
# 删除名为 bigdataserver 的会话
tmux kill-session -t bigdataserver
```





