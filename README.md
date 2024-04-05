# 项目预览

http://47.116.207.105:8080

## 服务器环境配置（已完成）

### 使用 VSCode 登录服务器

使用 `vscode` 的 `Remote-SSH` 插件远程登录服务器

### 配置MiniConda

```
# 下载 miniconda 安装包
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh
# 安装 miniconda 
bash Miniconda3-py39_24.1.2-0-Linux-x86_64.sh
# 初始化 miniconda
source ~/.bashrc
```

### 配置Python以及Django

```
# 创建 python 虚拟环境
conda create --name bigdata python=3.10
# 激活 python 虚拟环境
conda activate bigdata
# 安装 python django 库，使用镜像源
pip install django -i https://mirrors.aliyun.com/pypi/simple/
```

### 创建并启动Django项目

```
# 新建名为 bigdata 的 django 项目
django-admin startproject bigdata
# 进入 django 项目
cd bigdata
# 进入开发模式，vscode 会将服务器端口转发到本地
python manage.py runserver
```

### Django基础配置

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

### 服务器后台运行服务

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

## 在线开发指南

这里的在线开发指的是直接登录我们的服务器，修改服务器里的代码，由于服务器里以及配置好了环境，并且通过`tmux`使server一直运行在服务器后台，所以在线开发，只需要修改相应的代码文件并保存，`django`的热重载就会将修改后的网页体现在网站上。

所以，线上开发通过`vscode`连接服务器修改代码，并直接在[http://47.116.207.105:8080](http://47.116.207.105:8080)得到修改的反馈。

需要注意服务器代码修改的不可逆性，修改当然可以通过`ctrl+z`回退，但误修改导致的程序BUG会让人头疼，所以遇到手动无法解决的代码回退问题，要用到`GIT`进行版本管理。在服务器上，已经配置了`ssh`私钥连接`github`，同步代码无需输入账号密码，所以建议在重大修改之前先进行代码版本的存储并同步至`github`。`github`仓库地址为
https://github.com/flyQQQHddd/bigdata

总之，基本步骤如下：

1. 使用`vscode`登录服务器
2. 重大修改前请使用`git`存储代码并同步至`github`
3. 修改代码，并在[http://47.116.207.105:8080](http://47.116.207.105:8080)查看修改反馈
4. 修改过后，退出服务器之前，请使用`git`提交代码并同步至`github`，这将有利于本地开发与在线开发的代码同步 


## 本地开发指南

这里的本地开发指的是将`github`上的代码`pull`至本地，在本地配置环境并进行开发，修改代码结束后使用`git`提交代码并同步至`github`，之后在服务器上`pull`代码即可。

本地需要配置的环境为`python`和`django`，详情见`# 服务器环境配置（已完成）`章节

## 项目框架

整体上，项目目前采用的框架是`django`（典型的`MVT`架构），但我们去掉了`MVT`中的`T(Templates)`，这是因为`django`中的`Templates`标记语法不利于前后端分离开发。`django`的基本教程请自行百度。

开发方面，我们采用前后端分离开发，前端基于最基本的`HTML`、`CSS`以及`JavaScript`语法，开发界面，后端使用`django`的`V(Views)`进行URL响应。

前后端交互方面，前端使用三件套搭建基本版式，并使用`Ajax`调用API请求数据，在前端通过`ECharts`进行数据的图表渲染。

后端URL响应方面，我们的URL响应分为两大类：

1. 用户基于浏览器的页面请求，例如`http://47.116.207.105:8080`，对于这类请求，后端返回对应页面的`HTML`、`CSS`以及`JavaScript`代码。这也就是我们最终要展示的成果。
2. 基于API的请求，例如`http://47.116.207.105:8080/api/`，前面提到我们的前端是通过`Ajax`调用API进行数据请求，对于这类请求，后端返回对应`JSON`格式的对象，供给前端进行渲染。（`Ajax`使用代码可以见test.html）

> 注：尽量使用`RESTful`风格的API，当然这应该不是这个赛道的重点

## 开发过程中的一些问题

### 静态资源
前端进行开发时，不可避免的使用一些静态资源，例如`CSS`、`PNG`、`JS`以及配置在服务器上的第三方库等等，这些会在`HTML`代码文件中以链接的形式存在。

当服务上线后，这些静态资源无法直接通过本地路径拿到，`django`提供了一个访问静态资源的URL，具体的使用方式如下：例如当想要在`HTML`中嵌入一个`favicon.png`文件时，先将该文件放在`bigdata/static`目录之下，具体地，可以放在`bigdata/static/img`目录之下，之后在`HTML`文件中，使用如下的代码：
```
<link href="http://47.116.207.105:8080/static/img/favicon.png" rel="icon">
```

简单而言：对于每一个位于`bigdata/static/`下的文件，都会生成一个在`http://47.116.207.105:8080/static`下的链接，指向该文件。

### 文件目录

- `bigdata/bigdata`：核心代码
   - `api.py`：实际上也是`views.py`的一部分，分出来是为了区分两大类URL（用户访问和API请求）
   - `urls.py`：所有URL与View的匹配均在这里进行
   - `views.py`：视图函数，即逻辑处理函数
- `bigdata/static`：静态资源
- `bigdata/templates`：HTML文件目录

### 前端开发

采用了前后端分离开发后，受益最大的就是前端，完全使用纯粹的`CSS`、`PNG`、`JS`以及`Ajax`进行开发。但要注意超链接的使用：不能使用本地路径，而要使用`# 静态资源`中提到的方法。

### 后端开发

后端开发主要负责两个方面：

1. URL与View的匹配
2. View函数的设计


### 大模型辅助编码

已经在服务器安装了`通义灵码`的`VSCode`插件，使用`VSCode`登录服务器，并在`VSCode`左侧`通义灵码`扩展按钮登录阿里云账号即可使用。真的非常强大，除过智能问答，还可以直接在代码文件中写注释，`通义灵码`会帮你完成对应的代码！

登录教程链接：
https://help.aliyun.com/document_detail/2593225.html